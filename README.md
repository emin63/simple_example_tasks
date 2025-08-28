
# Introduction

This is a simple project to show how you can use
[ox_task](https://github.com/aocks/ox_task) to easily and
automatically run personal tasks in the cloud using GitHub actions.

With a few simple steps you can configure your own weather alerts or
news alerts or other computing tasks.

## Benefits

Some benefits of using `ox_task` with GitHub actions include:

  1. Programmers can easily create simple scripts or complex commands which run in the cloud (including a generous amount of free computing minutes from GitHub).
  2. Non-programmers can easily fork examples and customize them or ask LLMs like ChatGPT, Gemini, or Claude to generate simple python scripts.
     - The benefit of `ox_task` with GitHub actions is that you can easily get your desired scripts running the cloud.
  3. Secret management, logs, etc., are generally easier than other cloud platforms.

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

If you want to customize how the alerts work, you have a few choices:

  1. Add environment variable definitions in your workflow file to control things like `LATITUDE`, `LONGITUDE`, `HOT_ALERT`, `COLD_ALERT`, etc., for the weather alert and things like `FEEDS` or `KEYWORDS` for the news alert.
  2. Modify the python scripts directly.
  3. Ask an AI like ChatGPT, Claude, or Gemini to make the modifications for you.
  
  

