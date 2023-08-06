# encoding: utf-8
# api: python
# type: init
# title: modseccfg
# description: Editor to tame mod_security rulesets
# version: 0.0.9
# state:   prototype
# support: none
# license: ASL
# depends: python:pysimplegui (>= 3.0), python:pluginconf (>= 0.7.2)
# priority: core
# url: https://fossil.include-once.org/modseccfg/
# category: config
# classifiers: x11, http
#
# Correlates mod_security SecRules to logs, and simplifies
# disabling unneeded rules. It's very basic and not gonna
# win any usability awards.
# BE WARNED THAT ALPHA RELEASES MAY DAMAGE YOUR APACHE SETUP.
#
# Basically you select your desired vhost *.conf file, then
# hit [Disable] for rules with a high error.log count - if it's
# false positives. Preferrably leave rules untouched that are
# indeed working as intended.
#


    