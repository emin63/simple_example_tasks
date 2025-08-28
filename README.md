
# Introduction

This is a simple project to show how you can use
[https://github.com/aocks/ox_task](ox_task) to easily and
automatically run personal tasks in the cloud using GitHub actions.

# Usage

To try this out, do the following:

  1. Fork this repo (click the `Fork` button in the upper right of the
     GitHub page for this project).
  2. Review the [workflows for this project](https://github.com/emin63/simple_example_tasks/tree/main/.github/workflows).
  3. Go to the `Actions` tab for your newly forked repo, and click on the button to enable forked workflows.
  4. In your `Settings` tab on GitHub, go to the
     `Security -> Secrets and Variables -> Actions` entry.
  5. Click on `New repository secret` button and add the following secrets:
     - `TO_EMAIL`: Email address you want alerts sent to.
	 - `FROM_EMAIL`: Your email account on GMail.
	 - `GMAIL_APP_PASSWD`: Your app password on GMail (e.g., see [instructions on how to create an app password](https://support.google.com/mail/thread/205453566/how-to-generate-an-app-password?hl=en)).
  
You workflow is now ready. By default it should run at 8 am New York
time each day.

You can test the workflow by going to the `Actions` and manually
triggering it (see
[GitHub docs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)).
