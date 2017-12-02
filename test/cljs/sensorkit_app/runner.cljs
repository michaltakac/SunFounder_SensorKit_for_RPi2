(ns sensorkit-app.runner
    (:require [doo.runner :refer-macros [doo-tests]]
              [sensorkit-app.core-test]))

(doo-tests 'sensorkit-app.core-test)
