Heroku buildpack: Scala
=========================

This is a [Heroku buildpack](http://devcenter.heroku.com/articles/buildpacks) for publishing a repo for Scala apps.
It uses [sbt](https://github.com/harrah/xsbt/) 0.11.0+.

Usage
-----

Example usage:

    $ ls
    target src

    $ heroku create --stack cedar --buildpack https://github.com/baloo/sbt-repo-buildpack.git

    $ git push heroku master
    ...
    -----> Heroku receiving push
    -----> Scala app detected
    -----> Building app with sbt
    -----> Running: sbt clean compile publish-local

Config
------
By default content will not be exposed on the internet to publish it:

    $ heroku config:add NO_AUTH=True

If you want to authenticate other people from your org on google apps set:

    $ heroku config:add DOMAIN=acme.com

License
-------

Licensed under the MIT License. See LICENSE file.
