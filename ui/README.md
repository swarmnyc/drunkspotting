DrunkSpotting Web App
=====================

Please reference this guide for setting up, using, and working on the web app project.

Installation
------------

The app is a PHP project.  We are using a simple, micro-framework called [Silex](http://silex.sensiolabs.org/).
Silex is actually a project based off of [Symfony2](http://symfony.com/doc/master/index.html). So it has a solid foundation, but is dead simple.

Also, with Symfony/Silex there is a great templating language called [Twig](twig.sensiolabs.org/) that is being used.  Docs are great, and it makes things very easy.

Requirements:

- PHP 5.3+
- cURL (including the PHP5 cURL module)
- ImageMagick (including the PHP5 Imagick module)

Step One:

    $ git clone https://github.com/drunkspotting/drunkspotting.git

Step Two:

    $ cd drunkspotting/ui

Step Three:

This step will install all dependencies.  This is identical to "bundle install" in the Ruby world.
Therefore, this step will require PHP to be installed.

    $ ./composer.phar install

Step Five:

I know its not the best practice to 777 anything, but in production, these folders and not in the web directory, so its safe.

    $ chmod -R 777 ui/cache ui/logs
    
Step Six:

Verify you have a default timezone set in your php.ini file, or you will get an exception thrown.

    date.timezone = America/New_York

Step Seven:

Setup some kind of local server, and make "./ui/web" the server root.

I believe that is the end.  You can hit "index_dev.php" for seeing development settings, and "index.php" for seeing production settings.  So "index_dev.php/about" would get you to the about page.  If you setup an Apache/Nginx server, then you can add rewrite rules, like the ones we have in production, so you do not have to type the index file name, but its not required.

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

As always, please contact James Solomon (solomonjames@gmail.com / 813-767-8117) if there are any questions.
