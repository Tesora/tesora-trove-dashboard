/**
 * Copyright 2016 IBM Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  angular
    .module('horizon.dashboard.project.backups')
    .controller('horizon.dashboard.project.backups.tableController', backupsTableController);

  backupsTableController.$inject = [
    '$scope',
    'horizon.app.core.openstack-service-api.trove',
    'horizon.dashboard.project.backups.tableConfigService'
  ];

  /**
   * @ngdoc controller
   * @name horizon.dashboard.project.backups.tableController
   *
   * @description
   * Controller for the backups table
   */

  function backupsTableController($scope, trove, config) {

    var ctrl = this;
    ctrl.config = config;
    ctrl.backups = [];
    ctrl.backupsSrc = [];

    init();

    //////////

    function init() {
      trove.getBackups().success(getBackupsSuccess);
    }

    function getBackupsSuccess(response) {
      ctrl.backups = response;
    }
  }

})();
