POLLY for AppEngine
===================

Welcome and thanks for your interest in POLLY for AppEngine.

Installing POLLY is simple, just create a 'polly' folder in any Google AppEngine application you own, download all the files from this repo to that folder, and add the following line to your app.yaml file:

    includes:
    - polly/app.yaml

That's it! It should work flawlessly. To try it out, just point your browser to yourapp/polly/admin using your Google ID since you will be the only administrator and from there you can start creating as many polls as you like. Once you have created at least one poll then you are ready for the next step.

To show polls in your web page or blog just add this to your sidebar:

    <iframe id="polly" src="/polly">

and that's it! The latest poll will show up automatically in your web page. If you want to show a particular poll, specify its ID like this:

    <iframe id="polly" src="/polly/v/{pollid}">

Simpler impossible. We hope you enjoy POLLY as much as we do. Polls are by default made to fit in 300px and have a basic style which can be customized to your taste changing the style.css stylesheet found in /polly folder

POLLY is an ongoing project with many more features coming along. Remember to check back once in a while for updates, or fork it if you want to improve it yourself.

Thanks again for using POLLY and feel free to send us any suggestions or bugs you may encounter.


POLLY TEAM.
