DrunkSpotting Web App
=====================

Please reference this guide for setting up, using, and working on the web app project.

As always, please contact James Solomon (solomonjames@gmail.com / 813-767-8117) if there are any questions.

Installation
------------

The app is a PHP project.  We are using a simple, micro-framework called [Silex](http://silex.sensiolabs.org/).
Silex is actually a project based off of [Symfony2](http://symfony.com/doc/master/index.html). So it has a solid foundation, but is dead simple.

Also, with Symfony/Silex there is a great templating language called [Twig](twig.sensiolabs.org/) that is being used.  Docs are great, and it makes things very easy.

__Requirements:__

- PHP 5.3+
- cURL (including the PHP5 cURL module)
- ImageMagick (including the PHP5 Imagick module)

__Step One:__

    $ git clone https://github.com/drunkspotting/drunkspotting.git

__Step Two:__

    $ cd drunkspotting/ui

__Step Three:__

This step will install all dependencies.  This is identical to "bundle install" in the Ruby world.
Therefore, this step will require PHP to be installed.

    $ ./composer.phar install && cd ../

__Step Five:__

I know its not the best practice to 777 anything, but in production, these folders and not in the web directory, so its safe.

    $ chmod -R 777 ui/cache ui/logs
    
__Step Six:__

Verify you have a default timezone set in your php.ini file, or you will get an exception thrown.

    date.timezone = America/New_York

__Step Seven:__

You will need to install Vagrant

    $ brew install vagrant

Or
    
    $ port install vagrant
    
Or

    $ gem install vagrant
    
Or visit this page and download the verions you need: [http://downloads.vagrantup.com/tags/v1.0.3]()

__Step Eight:__

    $ vagrant up
    
This should download the VM box, import it, and then provision it with Puppet, all in one step.

__Step Nine:__

    $ sudo vim /etc/hosts
    
And add this line to the end:

    192.168.33.98 local.drunkspotting.com
    
And boom you should be able to hit: [http://local.drunkspotting.com]() and it load right up.  This will mimic production with an nginx server proxying to php5-fpm.

Folder Explanation
------------------

Directory structure

- ./ui/web : The directory that should be your web root.
 - /index.php : Loads prod settings
 - /index_dev.php : Loads dev settings
- ./ui/vendor : Where all the dependencies will live. Where composer installs everything.
- ./ui/templates : This is where templates, used by controllers, will live. They say .html, but they are actually being parsed as Twig template files.
 - /layout.html : This is the main layout, that all the other templates will inherit from.
- ./ui/src : Here is where the main app things happen
 - /app.php : Sets up the Application object
 - /console.php : Sets up the console commands, so you can write CLI operations using Symfony
 - /controllers.php : This is what defines each page in the app and how to render them, load them. 
- ./ui/logs : By default, in dev, Symfony writes nice, verbose logs for debugging
- ./ui/config : Setting up environment specific settings, dev inherits from prod
- ./ui/cache : Is a folder Symfony will write to to cache certain things for performance gains.  Caching is mainly performed in production mode.

Current Issues
--------------

We are still connecting to the production backend service, which isn't good for testing, but more of an issue, causes a cross server error with the cavnas element.  So you can just edit your /etc/hosts file to allow your local server to work as something like "local.drunkspotting.com" and that will work.

    $ sudo vim /etc/hosts
    
And then add a line like this to the end (with the proper IP address): 127.0.0.1 local.drunkspotting.com

Tricks
------

You can skip the upload process and load a local image by running the following command in the web console:

    $('#edit-panel').show(); drunkspotting.init_drawing('/assets/img/[image_here]');


Development Process
-------------------

1. Find an issue on Github (or create one if its not there).
2. Assign it to yourself
3. Update master branch, then do `$ git checkout -b issue-xx` with your issue #.
4. When you make commits (ideally just one large one) make sure to tag it with your issue number like this `git com -m "[Issue #1] : Message"` this way the ticket gets linked to the commit.
5. Push the branch to origin
6. Once you are done, issue a pull requst for master from your branch.

Eventually staging.drunkspotting will auto update from master, and we will do manual updates to production.

If there are any thoughts/questions on this, please contact me.  So far it seems like it will be the best to keep us from stepping on each other and still get shit done.
