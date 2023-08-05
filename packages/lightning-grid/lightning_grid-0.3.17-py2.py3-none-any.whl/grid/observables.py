import ast
import click
import websockets

import grid.globals as env
from gql import gql
from gql.transport.exceptions import TransportQueryError
from shlex import split
from yaspin import yaspin
from datetime import datetime, timezone
from typing import Optional, List
from rich.console import Console
from dateutil.parser import parse as date_string_parse
from grid.utilities import (get_abs_time_difference, string_format_timedelta,
                            get_param_values, get_experiment_duration_string)

from rich.table import Table
from rich.progress import (BarColumn, TextColumn, Progress)

#  Maps backend class types to user-friendly messages.s
TASK_CLASS_MAPPING = {
    'grid.core.repository_builder.RepositoryBuilder':
    'Building container',
    'grid.core.cluster.Cluster':
    'Creating cluster',
    'grid.core.trainer.experiment.Experiment':
    'Scheduling experiment',
    'grid.core.trainer.run.RunNodePool':
    'Creating node pool',
    'grid.core.trainer.interactive.InteractiveNodeTask':
    'Creating interactive node'
}


def style_status(format_string: str, status: str):
    """
    Styles a status message using click.stye.

    Parameters
    ----------
    status: str
        Status message to style.

    Return
    ------
    styled_status: str
        Styled string
    """
    styled_status = format_string

    if status == 'failed':
        styled_status = click.style(styled_status, fg='red')
    elif status in ('finished', 'ready'):
        styled_status = click.style(styled_status, fg='green')
    elif status in ('running', 'queued', 'pending'):
        styled_status = click.style(styled_status, fg='yellow')
    elif status in ('cancelled'):
        styled_status = click.style(styled_status, fg='white')

    return styled_status


class BaseObservable:
    def __init__(self, client, spinner_load_type=""):
        self.client = client
        self.console = Console()
        self.spinner = yaspin(text=f"Loading {spinner_load_type}...",
                              color="yellow")

    @staticmethod
    def create_table(columns: List[str]) -> Table:
        table = Table(show_header=True, header_style="bold green")

        table.add_column(columns[0], style='dim')
        for column in columns[1:]:
            table.add_column(column, justify='right')

        return table

    def _get_task_run_dependencies(self, run_id: str):
        """Gets dependency data for a given Run"""
        query = gql("""
        query (
            $runName: ID!
        ) {
            getRunTaskStatus (
                runName: $runName
            ) {
                runId
                name
                status
                message
                dependencies {
                    taskId
                    status
                    taskType
                    message
                    error
                }
            }
        }
        """)
        params = {'runName': run_id}

        #  Make GraphQL query.
        result = None
        try:
            result = self.client.execute(query, variable_values=params)
        except Exception as e:  # skipcq: PYL-W0703
            message = ast.literal_eval(str(e))['message']
            self.spinner.fail("✘")

            if env.DEBUG:
                click.echo(message)

            if 'not found' in message:
                raise click.ClickException(
                    f'Run {run_id} not found. Did you cancel it already?')

        if result:
            dependencies = result['getRunTaskStatus']['dependencies']
            return dependencies

    def _get_task_run_status(self, run_id: str):
        #  Get dependency data.
        dependencies = self._get_task_run_dependencies(run_id=run_id)

        #  Dict to collect all errors for given tasks.
        dependency_data = {
            k: {
                'statuses': [],
                'errors': [],
                'messages': []
            }
            for k in TASK_CLASS_MAPPING
        }
        for task in dependencies:
            dependency_data[task['taskType']]['statuses'].append(
                task['status'])
            dependency_data[task['taskType']]['errors'].append(task['error'])
            dependency_data[task['taskType']]['messages'].append(
                task['message'])

        #  Inform user that she can see error logs by passing
        #  a flag.
        all_statuses = []
        for status in dependency_data.values():
            all_statuses += status['statuses']

        if any(s == 'failed' for s in all_statuses) and \
            not env.SHOW_PROCESS_STATUS_DETAILS:
            click.echo(f'''
        The Run "{run_id}" failed to start due to a setup error.
        You can see the errors by running

            grid status {run_id} --details

            ''')

        #  Create progress bar.
        click.echo('\n')
        with Progress(
                TextColumn("[bold blue]{task.description}", justify="left"),
                BarColumn(bar_width=55),
                "[self.progress.percentage]{task.percentage:>3.1f}%"
        ) as progress_bar:

            #  Render progress bar based on finished tasks.
            task_id = progress_bar.add_task('Submitting Run',
                                            start=True,
                                            total=len(all_statuses))
            # progress.start_task(task_id)
            progress = sum(1 for s in all_statuses if s == 'finished')
            progress_bar.update(task_id, advance=progress)

        #  If there's an error with creating a cluster, then
        #  print that error to the terminal.
        if env.SHOW_PROCESS_STATUS_DETAILS:
            for key, value in dependency_data.items():
                for error, message, status in zip(value['errors'],
                                                  value['messages'],
                                                  all_statuses):
                    styled_key = style_status(TASK_CLASS_MAPPING[key], status)
                    if error:
                        for line in error.splitlines():
                            click.echo(f'[{styled_key}] {line}')
                    else:
                        click.echo(f'[{styled_key}] {message} ... ')


class Run(BaseObservable):
    def __init__(self, client: 'Grid', identifier: Optional[str] = []):
        self.client = client

        self.identifier = identifier

        super().__init__(client=client, spinner_load_type="Runs")

    def get(self):
        """
        Gets the run status; either for a single run or all runs for
        user.
        """
        self.spinner.start()
        self.spinner.text = 'Getting Run status ...'

        query = gql("""
        query (
            $runId: ID
        ) {
            getRuns (runId: $runId) {
                name
                createdAt
                experiments {
                    experimentId
                }
                nExperiments
                nFailed
                nCancelled
                nRunning
                nCompleted
                nQueued
                projectId
                resourceUrls {
                    tensorboard
                }
            }
        }
        """)
        run_id = None
        if self.identifier:
            run_id = self.identifier

        params = {'runId': run_id}

        try:
            result = self.client.execute(query, variable_values=params)
            self.spinner.text = 'Done!'
        except TransportQueryError as e:
            self.spinner.fail("✘")
            self.spinner.stop()
            if env.DEBUG:
                click.echo(str(e))

            raise click.ClickException(
                'Query to Grid failed. Try in a few seconds?')

        table_cols = [
            'Run',
            'Project',
            'Status',
            'Duration',
            'Experiments',
            'Running',
            'Queued',
            'Completed',
            'Failed',
            'Cancelled',
        ]
        table = BaseObservable.create_table(columns=table_cols)

        #  Whenever we don't have yet submitted experiments,
        table_rows = 0
        for row in result['getRuns']:
            status = None

            # we only have 3 statuses for runs
            # running (if something is running)
            is_running = row['nRunning'] is not None and row['nRunning'] > 0

            # quued if there are queued elements
            is_queued = row['nQueued'] is not None and row['nQueued'] > 0

            # otherwise, everything else is history
            if is_queued:
                status = 'queued'
            elif is_running:
                status = 'running'
            else:
                # don't render table because it should be in history
                continue

            #  Change the printed key from `None` to `-` if the
            #  no data exists for those keys.
            keys = [
                'nExperiments', 'nRunning', 'nQueued', 'nCompleted', 'nFailed',
                'nCancelled'
            ]
            for key in keys:
                if row[key] is None:
                    row[key] = '-'

            # Calculate the duration column
            created_at = date_string_parse(row['createdAt'])
            delta = get_abs_time_difference(datetime.now(timezone.utc),
                                            created_at)
            duration_str = string_format_timedelta(delta)

            table.add_row(row['name'], row['projectId'], status, duration_str,
                          str(row['nExperiments']), str(row['nRunning']),
                          str(row['nQueued']), str(row['nCompleted']),
                          str(row['nFailed']), str(row['nCancelled']))

            #  Let's count how many rows have been added.
            table_rows += 1

        #  Close the spinner.
        self.spinner.ok("✔")
        self.spinner.stop()

        # If there are no Runs to render, add a
        # placeholder row indicating none are active.
        if not table_rows:
            table.add_row("None Active.",
                          *[" " for i in range(len(table_cols) - 1)])

        self.console.print(table)

        #  Print useful message indicating that users can run
        #  grid history.
        history_runs = len(result['getRuns']) - table_rows
        if history_runs > 0:
            click.echo(
                f'\n{history_runs} Run(s) are not active. Use `grid history` to view your Run history.'
            )

        return result

    def get_history(self):
        """
        Fetches a complete history of runs. This includes runs that
        are not currently active.
        """
        self.spinner.start()
        self.spinner.text = 'Getting Runs ...'

        query = gql("""
        query (
            $runId: ID
        ) {
            getRuns (runId: $runId) {
                name
                createdAt
                experiments {
                    experimentId
                }
                nExperiments
                nFailed
                nCancelled
                nRunning
                nCompleted
                nQueued
            }
        }
        """)
        run_id = None
        if self.identifier:
            run_id = self.identifier[0]

        params = {'runId': run_id}

        result = self.client.execute(query, variable_values=params)

        self.spinner.text = 'Done!'
        self.spinner.ok("✔")
        self.spinner.stop()

        table_cols = [
            'Run', 'Duration', 'Experiments', 'Failed', 'Cancelled',
            'Completed'
        ]
        table = BaseObservable.create_table(columns=table_cols)

        #  Whenever we don't have yet submitted experiments,
        table_rows = result['getRuns']
        for row in table_rows:
            keys = ['nExperiments', 'nFailed', 'nCancelled', 'nCompleted']
            for key in keys:
                if row[key] is None:
                    row[key] = '-'

            # check if it is running
            is_running = row['nRunning'] is not None and row['nRunning'] > 0

            # check if queued
            is_queued = row['nQueued'] is not None and row['nQueued'] > 0

            # history is everything else
            if is_queued or is_running:
                continue

            created_at = date_string_parse(row['createdAt'])

            delta = get_abs_time_difference(datetime.now(timezone.utc),
                                            created_at)
            duration_str = string_format_timedelta(delta)
            table.add_row(row['name'], duration_str, str(row['nExperiments']),
                          str(row['nFailed']), str(row['nCancelled']),
                          str(row['nCompleted']))

        # Add placeholder row if no records are available.
        if not table_rows:
            table.add_row("None Active.",
                          *[" " for i in range(len(table_cols) - 1)])

        self.spinner.ok("✔")
        self.console.print(table)

        return result

    def follow(self):
        pass


class Experiment(BaseObservable):
    def __init__(self, client: 'Grid', identifier: str):
        self.client = client
        self.run_id = identifier

        super().__init__(client=client)

    def get_history(self, experiment_id: Optional[str] = None):
        """
        Parameters
        ----------
        experiment_id: Optional[str]
            Experiment ID
        """
        self.spinner.start()
        self.spinner.text = 'Getting Experiments ...'

        query = gql("""
        query (
            $runId: ID!
        ) {
            getExperiments(runId: $runId) {
                experimentId
                status
                invocationCommands
                createdAt
                finishedAt
                commitSha
                run {
                    runId
                }
                startedRunningAt
            }
        }
        """)
        params = {'runId': self.run_id}
        try:
            self._get_task_run_status(run_id=self.run_id)
        except ValueError:
            return

        result = self.client.execute(query, variable_values=params)

        if not result['getExperiments']:
            click.echo(f'No experiments available for run "{self.run_id}"')
            return

        table = BaseObservable.create_table(
            columns=['Experiment', 'Status', 'Duration', 'Command'])

        experiments = result['getExperiments']

        self.spinner.text = 'Done!'
        self.spinner.ok("✔")
        self.spinner.stop()

        # If there are experiments to print,
        # show each hyperparam in it's own column
        if experiments:
            command = experiments[0]['invocationCommands']
            hparams = get_param_values(command)

            table_columns = ['Experiment', 'Status', 'Duration'] + hparams
            table = BaseObservable.create_table(columns=table_columns)

            for row in result['getExperiments']:
                # Split hparam vals
                command = row['invocationCommands']
                hparam_vals = get_param_values(command)

                # If queued use created time for the duration, if running use start time
                duration_str = get_experiment_duration_string(
                    created_at=row['createdAt'],
                    started_running_at=row['startedRunningAt'],
                    finished_at=row['finishedAt'])

                table.add_row(row['experimentId'], row['status'], duration_str,
                              *hparam_vals)

        self.console.print(table)

    def get(self, experiment_id: Optional[str] = None):
        """
        Parameters
        ----------
        experiment_id: Optional[str]
            Experiment ID
        """
        self.spinner.start()
        self.spinner.text = 'Fetching experiment status ...'

        query = gql("""
        query (
            $runId: ID!
        ) {
            getExperiments(runId: $runId) {
                experimentId
                status
                invocationCommands
                createdAt
                finishedAt
                commitSha
                run {
                    runId
                }
                startedRunningAt
            }
        }
        """)
        params = {'runId': self.run_id}
        try:
            self.spinner.text = 'Fetching experiment status ... done!'
            self.spinner.ok("✔")
            self.spinner.stop()
            self._get_task_run_status(run_id=self.run_id)
        except ValueError:
            return

        result = self.client.execute(query, variable_values=params)

        if not result['getExperiments']:
            click.echo(f'No experiments available for run "{self.run_id}"')
            return

        table = BaseObservable.create_table(
            columns=['Experiment', 'Status', 'Duration', 'Command'])

        experiments = result['getExperiments']

        # If there are experiments to print,
        # show each hyperparam in it's own column
        if experiments:
            command = experiments[0]['invocationCommands']
            toks = split(command)
            hparams = [tok.replace('--', '') for tok in toks if '--' in tok]

            table_columns = ['Experiment', 'Status', 'Duration'] + hparams
            table = BaseObservable.create_table(columns=table_columns)

            for row in result['getExperiments']:
                # Split hparam vals
                command = row['invocationCommands']
                hparam_vals = get_param_values(command)
                # Get job duration - Since experiment started if running, since experiment created if queued
                duration_str = get_experiment_duration_string(
                    created_at=row['createdAt'],
                    started_running_at=row['startedRunningAt'],
                    finished_at=row['finishedAt'])

                table.add_row(row['experimentId'], row['status'], duration_str,
                              *hparam_vals)

        self.console.print(table)

        return result

    def follow(self):
        """Follows a stream for a given Run."""
        self.spinner.text = 'Following Run details ...'
        self.spinner.start()

        #  Defines terminal states.
        terminal_state = ('finished', 'failed', 'cancelled')

        #  Get list of dependency IDs.
        dependencies = self._get_task_run_dependencies(run_id=self.run_id)
        dependency_ids = []
        dependency_statuses = []
        dependency_mapping = {}
        for dependency in dependencies:
            status = dependency['status']
            dependency_statuses.append(status)
            if status not in terminal_state:
                dependency_ids.append(dependency['taskId'])
                dependency_mapping[dependency['taskId']] = dependency

        #  Shows useful message to user.
        if all(s in terminal_state for s in dependency_statuses):
            self.spinner.ok("✔")
            self.spinner.stop()

            error_message = ''
            if any(s == 'failed' for s in dependency_statuses):
                error_message = """To see errors, run:

        grid status {self.run_id} --details"""

            click.echo(f"""

    Run ({self.run_id}) has finished scheduling in cluster.
    {error_message}
    """)
            self.get()
            raise click.ClickException('No scheduling steps to follow.\n')

        # If experiments are not in a terminal state,
        # open a websocket connection and consume messages.
        subscription = gql("""
        subscription GetTaskStream ($taskIds: [ID]!) {
            getTaskMessage(
                taskIds: $taskIds) {
                    taskId
                    message
                    timestamp
                    className
            }
        }
        """)

        params = {'taskIds': dependency_ids}

        #  Create a GraphQL subscription via websockect
        #  connection.
        try:
            stream = self.client.subscribe(subscription,
                                           variable_values=params)

            first_message = True
            for log in stream:

                #  Closes the spinner.
                if first_message:
                    self.spinner.text = 'Done!'
                    self.spinner.ok("✔")
                    first_message = False

                #  Patch a class name if not available with
                #  a placeholder.
                class_name = log['getTaskMessage']['className']
                if not class_name:
                    class_name = '-' * 10
                else:
                    class_name = TASK_CLASS_MAPPING[class_name]

                #  Extract task ID and status.
                task_id = log['getTaskMessage']['taskId']
                task_status = dependency_mapping[task_id]['status']

                #  Print each line to terminal.
                styled_class_name = style_status(class_name, task_status)
                message = log['getTaskMessage']['message']
                click.echo(f'[{styled_class_name}] {message}')

        # If connection is suddenly closed, indicate that a
        # known error happened.
        except websockets.exceptions.ConnectionClosedError:
            self.spinner.fail("✘")
            self.spinner.stop()
            raise click.ClickException('Could not fetch log data.')

        except websockets.exceptions.ConnectionClosedOK:
            self.spinner.fail("✘")
            self.spinner.stop()
            raise click.ClickException(
                'Could not continue fetching log stream.')

        #  Raise any other errors that the backend may raise.
        except Exception as e:  # skipcq: PYL-W0703
            self.spinner.fail("✘")
            self.spinner.stop()
            if 'Server error:' in str(e):
                e = str(e).replace('Server error: ', '')[1:-1]

            message = ast.literal_eval(str(e))['message']
            raise click.ClickException(message)


class InteractiveNode(BaseObservable):
    """
    Base observable for a Grid interactive node.

    Parameters
    ----------
    client: Grid
        Grid client
    project_id: str
        Project ID
    """
    def __init__(self, client: 'Grid'):
        self.client = client

        super().__init__(client=client, spinner_load_type="Interactive Nodes")

    def _get_task_status(self, interactive_node_id: str):
        """
        Gets task status for a given interactive node.

        Parameters
        ----------
        interactive_node_id: str
            Interactive node ID.
        """
        self.spinner.start()

        query = gql("""
        query GetInteractiveTaskStatus ($interactiveNodeId: ID!) {
            getInteractiveTaskStatus(interactiveNodeId: $interactiveNodeId) {
                status
                message
                dependencies {
                    taskId
                    status
                    taskType
                    message
                    error
                }
            }
        }
        """)
        params = {'interactiveNodeId': interactive_node_id}

        try:
            result = self.client.execute(query, variable_values=params)
        except Exception as e:  # skipcq: PYL-W0703
            message = ast.literal_eval(str(e))['message']
            self.spinner.fail("✘")
            raise click.ClickException(message)

        # Gets dependenceis.
        dependencies = result['getRunTaskStatus']['dependencies']

        #  Figure out the status of each task.
        dependency_data = {}
        for task in dependencies:
            dependency_data[task['taskType']] = {
                'status': task['status'],
                'error': task['error'],
                'message': task['message'],
                'status_message': TASK_CLASS_MAPPING[task['taskType']]
            }

        #  Display the status of setting-up the cluster & environment
        #  to the user.
        self.spinner.text = 'Done!'
        self.spinner.ok("✔")

        #  Show message if there's an error in a pre-start task.
        all_status = [s['status'] for s in dependency_data.values()]
        if any(s == 'failed' for s in all_status) and \
            not env.SHOW_PROCESS_STATUS_DETAILS:
            click.echo(f'''
        The Interactive Node "{interactive_node_id}" failed to start due to a setup error.
        You can see the errors by running

            grid status {interactive_node_id} --details

            ''')

        #  Create progress bar.
        click.echo('\n')
        with Progress(
                TextColumn("[bold blue]{task.description}", justify="left"),
                BarColumn(bar_width=55),
                "[self.progress.percentage]{task.percentage:>3.1f}%"
        ) as progress_bar:

            #  Render progress bar based on finished tasks.
            task_id = progress_bar.add_task('Creating Interactive Node',
                                            start=True,
                                            total=len(all_status))

            progress = sum(1 for s in all_status if s == 'finished')
            progress_bar.update(task_id, advance=progress)

        #  If there's an error with creating a cluster, then
        #  print that error to the terminal.
        if env.SHOW_PROCESS_STATUS_DETAILS:
            for key, value in dependency_data.items():
                if value.get('error'):
                    styled_key = click.style(TASK_CLASS_MAPPING[key], fg='red')
                    error = value.get('error')
                    for line in error.splitlines():
                        click.echo(f'[{styled_key}] {line}')
                else:
                    styled_key = click.style(TASK_CLASS_MAPPING[key],
                                             fg='green')
                    message = value.get('message')
                    click.echo(f'[{styled_key}] {message} ... ')

    def get(self):
        self.spinner.start()
        query = gql("""
        query GetInteractiveNodes{
            getInteractiveNodes {
                interactiveNodeId
                clusterId
                createdAt,
                projectId
                jupyterlabUrls
                status
                config {
                    diskSize
                    instanceType
                }
            }
        }
        """)

        result = {}

        try:
            result = self.client.execute(query)

            if not result['getInteractiveNodes']:
                self.spinner.fail("✘")
                if env.DEBUG:
                    click.echo(result['getInteractiveNodes'])
            else:
                self.spinner.ok("✔")

        #  Raise any other errors that the backend may raise.
        except TransportQueryError:  # skipcq: PYL-W0703
            self.spinner.fail("✘")

        # Create table with results.
        table_rows = 0
        table_cols = [
            'Project', 'Name', 'Status', 'Instance Type', 'Duration', 'URL'
        ]
        table = BaseObservable.create_table(columns=table_cols)

        if result and result['getInteractiveNodes']:
            for row in result['getInteractiveNodes']:
                # Fetch the first URL returned from backend.
                # TODO: Change to use FQDN.
                url = '-'
                if row['jupyterlabUrls']:
                    url = row['jupyterlabUrls'][0]

                # Calculate how long the interactive node has been up.
                created_at = date_string_parse(row['createdAt'])
                delta = get_abs_time_difference(datetime.now(timezone.utc),
                                                created_at)
                duration_str = string_format_timedelta(delta)

                # Add rows to table.
                if row['status'] == 'finished':
                    status = 'ready'
                else:
                    status = row['status']

                # Replace anything that doesn't have data with
                # a placeholder '-'.
                all_rows = [
                    row['projectId'], row['interactiveNodeId'], status,
                    row['config']['instanceType'], duration_str, url
                ]
                all_rows = ['-' if not r else r for r in all_rows]
                table.add_row(*all_rows)

                # Adds iterator
                table_rows += 1

        #  Close the spinner.
        self.spinner.stop()

        # If there are no nodes active, add a
        # placeholder row indicating that.
        if not table_rows:
            table.add_row("None Active.",
                          *[" " for i in range(len(table_cols) - 1)])

        # Print table
        self.console.print(table)

    def follow(self):
        pass
