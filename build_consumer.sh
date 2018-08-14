#!/bin/sh
cd $TRAVIS_BUILD_DIR/consumer
sbt ++$TRAVIS_SCALA_VERSION package