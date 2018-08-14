#!/bin/sh
cd $TRAVIS_BUILD_DIR/producer
sbt ++$TRAVIS_SCALA_VERSION package