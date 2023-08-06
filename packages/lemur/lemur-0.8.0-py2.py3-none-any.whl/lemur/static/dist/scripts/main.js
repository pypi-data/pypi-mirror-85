'use strict';

(function() {
  var lemur = angular
    .module('lemur', [
      'ui.router',
      'ngTable',
      'ngAnimate',
      'chart.js',
      'restangular',
      'angular-loading-bar',
      'ui.bootstrap',
      'toaster',
      'uiSwitch',
      'mgo-angular-wizard',
      'satellizer',
      'ngLetterAvatar',
      'angular-clipboard',
      'ngFileSaver',
      'ngSanitize',
      'ui.select'
    ]);


  function fetchData() {
    var initInjector = angular.injector(['ng']);
    var $http = initInjector.get('$http');

    return $http.get('/api/1/auth/providers').then(function(response) {
      lemur.constant('providers', response.data);
    }, function(errorResponse) {
      console.log('Could not fetch SSO providers' + errorResponse);
    });
  }

  function bootstrapApplication() {
    angular.element(document).ready(function() {
      angular.bootstrap(document, ['lemur']);
    });
  }

  fetchData().then(bootstrapApplication);

  lemur.config(function ($stateProvider, $urlRouterProvider, $authProvider, providers) {
    $urlRouterProvider.otherwise('/welcome');
    $stateProvider
      .state('welcome', {
        url: '/welcome',
        templateUrl: 'angular/welcome/welcome.html'
      });

    _.each(providers, function(provider) {
      if ($authProvider.hasOwnProperty(provider.name)) {
        $authProvider[provider.name](provider);
      } else {
        $authProvider.oauth2(provider);
      }
    });
  });

  lemur.directive('compareTo', function() {
    return {
        require: 'ngModel',
        scope: {
            otherModelValue: '=compareTo'
        },
        link: function(scope, element, attributes, ngModel) {

            ngModel.$validators.compareTo = function(modelValue) {
                return modelValue === scope.otherModelValue;
            };

            scope.$watch('otherModelValue', function() {
                ngModel.$validate();
            });
        }
    };
  });

  lemur.service('MomentService', function () {
    this.diffMoment = function (start, end) {
      if (end !== 'None') {
        return moment(end, 'YYYY-MM-DD HH:mm Z').diff(moment(start, 'YYYY-MM-DD HH:mm Z'), 'minutes') + ' minutes';
      }
      return 'Unknown';
    };
    this.createMoment = function (date) {
      if (date !== 'None') {
        return moment(date, 'YYYY-MM-DD HH:mm Z').fromNow();
      }
      return 'Unknown';
    };
  });

  lemur.controller('datePickerController', function ($scope, $timeout){
    $scope.open = function() {
      $timeout(function() {
        $scope.opened = true;
      });
    };
  });

  lemur.service('DefaultService', function (LemurRestangular) {
    var DefaultService = this;
    DefaultService.get = function () {
      return LemurRestangular.all('defaults').customGET().then(function (defaults) {
        return defaults;
      });
    };
  });

  lemur.service('DnsProviders', function (LemurRestangular) {
    var DnsProviders = this;
    DnsProviders.get = function () {
      return LemurRestangular.all('dns_providers').customGET().then(function (dnsProviders) {
        return dnsProviders;
      });
    };
  });

  lemur.directive('lemurBadRequest', [function () {
			return {
				template: '<h4>{{ directiveData.message }}</h4>' +
									'<div ng-repeat="(key, value) in directiveData.reasons">' +
										'<strong>{{ key | titleCase }}</strong> - {{ value }}</strong>' +
				          '</div>'
			};
		}]);

  lemur.factory('LemurRestangular', function (Restangular, $location, $auth) {
    return Restangular.withConfig(function (RestangularConfigurer) {
      RestangularConfigurer.setBaseUrl('/api/1');
      RestangularConfigurer.setDefaultHttpFields({withCredentials: true});

      // handle situation where our token has become invalid.
      RestangularConfigurer.setErrorInterceptor(function (response) {
        if (response.status === 401) {
          $auth.logout();
          $location.path('/login');
          return false;
        }
      });

      RestangularConfigurer.addResponseInterceptor(function (data, operation) {
        var extractedData;

        // .. to look for getList operations
        if (operation === 'getList') {
          // .. and handle the data and meta data
          extractedData = data.items;
          extractedData.total = data.total;
        } else {
          extractedData = data;
        }

        return extractedData;
      });

      RestangularConfigurer.addFullRequestInterceptor(function (element, operation, route, url, headers, params) {
        // We want to make sure the user is auth'd before any requests
        if (!$auth.isAuthenticated()) {
          $location.path('/login');
          return false;
        }

        var regExp = /\[([^)]+)\]/;

        var s = 'sorting';
        var f = 'filter';
        var newParams = {};
        for (var item in params) {
          if (item.indexOf(s) > -1) {
            newParams.sortBy = regExp.exec(item)[1];
            newParams.sortDir = params[item];
          } else if (item.indexOf(f) > -1) {
            var key = regExp.exec(item)[1];
            newParams.filter = key + ';' + params[item];
          } else {
            newParams[item] = params[item];
          }
        }
        return { params: newParams };
      });

    });
  });

  lemur.run(function ($templateCache, $location, $rootScope, $auth, $state) {
    $templateCache.put('ng-table/pager.html', '<div class="ng-cloak ng-table-pager"> <div ng-if="params.settings().counts.length" class="ng-table-counts btn-group pull-left"> <button ng-repeat="count in params.settings().counts" type="button" ng-class="{\'active\':params.count()==count}" ng-click="params.count(count)" class="btn btn-default"> <span ng-bind="count"></span> </button></div><div class="pull-right"><ul style="margin: 0; padding: 0;" class="pagination ng-table-pagination"> <li ng-class="{\'disabled\': !page.active}" ng-repeat="page in pages" ng-switch="page.type"> <a ng-switch-when="prev" ng-click="params.page(page.number)" href="">&laquo;</a> <a ng-switch-when="first" ng-click="params.page(page.number)" href=""><span ng-bind="page.number"></span></a> <a ng-switch-when="page" ng-click="params.page(page.number)" href=""><span ng-bind="page.number"></span></a> <a ng-switch-when="more" ng-click="params.page(page.number)" href="">&#8230;</a> <a ng-switch-when="last" ng-click="params.page(page.number)" href=""><span ng-bind="page.number"></span></a> <a ng-switch-when="next" ng-click="params.page(page.number)" href="">&raquo;</a> </li> </ul> </div></div>');
    $rootScope.$on('$stateChangeStart', function(event, toState, toParams) {
      if (toState.name !== 'login') {
        if (!$auth.isAuthenticated()) {
          event.preventDefault();
          $state.go('login', {'toState': toState.name, 'toParams': toParams, notify: false});
        }
      }
    });
  });
}());



'use strict';

angular.module('lemur')
  .service('ApiKeyApi', function (LemurRestangular) {
    LemurRestangular.extendModel('keys', function (obj) {
      return angular.extend(obj, {
        attachUser: function (user) {
          this.user = user;
        }
      });
    });
    return LemurRestangular.all('keys');
  })
  .service('ApiKeyService', function ($location, ApiKeyApi) {
    var ApiKeyService = this;

    ApiKeyService.update = function(apiKey) {
      return apiKey.put();
    };

    ApiKeyService.create = function (apiKey) {
      return ApiKeyApi.post(apiKey);
    };

    ApiKeyService.delete = function (apiKey) {
      return apiKey.remove();
    };
  });

'use strict';
angular.module('lemur')
  .service('AuthorityApi', function (LemurRestangular) {
    LemurRestangular.extendModel('authorities', function (obj) {
      return angular.extend(obj, {
        attachRole: function (role) {
          this.selectedRole = null;
          if (this.roles === undefined) {
            this.roles = [];
          }
          this.roles.push(role);
        },
        removeRole: function (index) {
          this.roles.splice(index, 1);
        },
        attachSubAltName: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.subAltNames === undefined) {
            this.extensions.subAltNames = {'names': []};
          }

          if (!angular.isString(this.subAltType)) {
            this.subAltType = 'DNSName';
          }

          if (angular.isString(this.subAltValue) && angular.isString(this.subAltType)) {
            this.extensions.subAltNames.names.push({'nameType': this.subAltType, 'value': this.subAltValue});
            //this.findDuplicates();
          }

          this.subAltType = null;
          this.subAltValue = null;
        },
        removeSubAltName: function (index) {
          this.extensions.subAltNames.names.splice(index, 1);
        },
        attachCustom: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.custom === undefined) {
            this.extensions.custom = [];
          }

          if (angular.isString(this.customOid) && angular.isString(this.customEncoding) && angular.isString(this.customValue)) {
            this.extensions.custom.push(
              {
                'oid': this.customOid,
                'isCritical': this.customIsCritical || false,
                'encoding': this.customEncoding,
                'value': this.customValue
              }
            );
          }

          this.customOid = null;
          this.customIsCritical = null;
          this.customEncoding = null;
          this.customValue = null;
        },
        removeCustom: function (index) {
          this.extensions.custom.splice(index, 1);
        },
        setEncipherOrDecipher: function (value) {
          if (this.extensions === undefined) {
            this.extensions = {};
          }
          if (this.extensions.keyUsage === undefined) {
            this.extensions.keyUsage = {};
          }
          var existingValue = this.extensions.keyUsage[value];
          if (existingValue) {
            // Clicked on the already-selected value
            this.extensions.keyUsage.useDecipherOnly = false;
            this.extensions.keyUsage.useEncipherOnly = false;
            // Uncheck both radio buttons
            this.encipherOrDecipher = false;
          } else {
            // Clicked a different value
            this.extensions.keyUsage.useKeyAgreement = true;
            if (value === 'useEncipherOnly') {
              this.extensions.keyUsage.useDecipherOnly = false;
              this.extensions.keyUsage.useEncipherOnly = true;
            } else {
              this.extensions.keyUsage.useEncipherOnly = false;
              this.extensions.keyUsage.useDecipherOnly = true;
            }
          }
        }
      });
    });
    return LemurRestangular.all('authorities');
  })
  .service('AuthorityService', function ($location, AuthorityApi, DefaultService) {
    var AuthorityService = this;
    AuthorityService.findAuthorityByName = function (filterValue) {
      return AuthorityApi.getList({'filter[name]': filterValue})
        .then(function (authorites) {
          return authorites;
        });
    };

    AuthorityService.findActiveAuthorityByName = function (filterValue) {
      return AuthorityApi.getList({'filter[name]': filterValue})
        .then(function (authorities) {
          return authorities.filter(function(authority) { return authority.active; });
        });
    };

    AuthorityService.create = function (authority) {
      authority.attachSubAltName();
      authority.attachCustom();

      if (authority.extensions.basicConstraints === undefined) {
        authority.extensions.basicConstraints = { 'path_length': null};
      }
      authority.extensions.basicConstraints.ca = true;
      if (authority.extensions.basicConstraints.path_length === 'None') {
        authority.extensions.basicConstraints.path_length = null;
      }

      if (authority.validityYears === '') { // if a user de-selects validity years we ignore it
        delete authority.validityYears;
      }
      return AuthorityApi.post(authority);
    };

    AuthorityService.update = function (authority) {
      return authority.put();
    };

    AuthorityService.getDefaults = function (authority) {
      return DefaultService.get().then(function (defaults) {
        authority.country = defaults.country;
        authority.state = defaults.state;
        authority.location = defaults.location;
        authority.organization = defaults.organization;
        authority.organizationalUnit = defaults.organizationalUnit;
        authority.defaultIssuerPlugin = defaults.issuerPlugin;
      });
    };

    AuthorityService.getRoles = function (authority) {
      return authority.getList('roles').then(function (roles) {
        authority.roles = roles;
      });
    };

    AuthorityService.updateActive = function (authority) {
      return authority.put();
    };

  });

'use strict';
angular.module('lemur')
  .service('AuthenticationApi', function (LemurRestangular) {
    return LemurRestangular.all('auth');
  })
  .service('AuthenticationService', function ($location, $rootScope, AuthenticationApi, UserService, toaster, $auth) {
    var AuthenticationService = this;

    AuthenticationService.login = function (username, password) {
      return AuthenticationApi.customPOST({'username': username, 'password': password}, 'login');
    };

    AuthenticationService.authenticate = function (provider) {
      return $auth.authenticate(provider);
    };

    AuthenticationService.logout = function () {
      if (!$auth.isAuthenticated()) {
        return;
      }
      $auth.logout()
        .then(function() {
          $rootScope.$emit('user:logout');
          toaster.pop({
            type: 'success',
            title: 'Good job!',
            body: 'You have been successfully logged out.'
          });
          $location.path('/login');
        });
    };
  });
'use strict';

angular.module('lemur').
  filter('titleCase', function () {
    return function (str) {
      return (str === undefined || str === null) ? '' : str.replace(/([A-Z])/g, ' $1').replace(/^./, function (txt) {
        return txt.toUpperCase();
      });
    };
  });


'use strict';

angular.module('lemur')
  .service('CertificateApi', function (LemurRestangular, DomainService) {
    LemurRestangular.extendModel('certificates', function (obj) {
      return angular.extend(obj, {
        attachRole: function (role) {
          this.selectedRole = null;
          if (this.roles === undefined) {
            this.roles = [];
          }
          this.roles.push(role);
        },
        removeRole: function (index) {
          this.roles.splice(index, 1);
        },
        attachAuthority: function (authority) {
          this.authority = authority;
          this.authority.maxDate = moment(this.authority.notAfter).subtract(1, 'days').format('YYYY/MM/DD');
        },
        attachCommonName: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.subAltNames === undefined) {
            this.extensions.subAltNames = {'names': []};
          }

          if (angular.isString(this.commonName)) {
            this.extensions.subAltNames.names.unshift({'nameType': 'DNSName', 'value': this.commonName});
          }
        },
        removeCommonName: function () {
          if (angular.isDefined(this.extensions) && angular.isDefined(this.extensions.subAltNames)) {
            if (angular.equals(this.extensions.subAltNames.names[0].value, this.commonName)) {
              this.extensions.subAltNames.names.shift();
            }
          }
        },
        attachSubAltName: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.subAltNames === undefined) {
            this.extensions.subAltNames = {'names': []};
          }

          if (!angular.isString(this.subAltType)) {
            this.subAltType = 'DNSName';
          }

          if (angular.isString(this.subAltValue) && angular.isString(this.subAltType)) {
            this.extensions.subAltNames.names.push({'nameType': this.subAltType, 'value': this.subAltValue});
            //this.findDuplicates();
          }

          this.subAltType = null;
          this.subAltValue = null;
        },
        removeSubAltName: function (index) {
          this.extensions.subAltNames.names.splice(index, 1);
          //this.findDuplicates();
        },
        attachCustom: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.custom === undefined) {
            this.extensions.custom = [];
          }

          if (angular.isString(this.customOid) && angular.isString(this.customEncoding) && angular.isString(this.customValue)) {
            this.extensions.custom.push(
              {
                'oid': this.customOid,
                'isCritical': this.customIsCritical || false,
                'encoding': this.customEncoding,
                'value': this.customValue
              }
            );
          }

          this.customOid = null;
          this.customIsCritical = null;
          this.customEncoding = null;
          this.customValue = null;
        },
        removeCustom: function (index) {
          this.extensions.custom.splice(index, 1);
        },
        attachDestination: function (destination) {
          this.selectedDestination = null;
          if (this.destinations === undefined) {
            this.destinations = [];
          }
          this.destinations.push(destination);
        },
        removeDestination: function (index) {
          this.destinations.splice(index, 1);
        },
        attachReplaces: function (replaces) {
          this.selectedReplaces = null;
          if (this.replaces === undefined) {
            this.replaces = [];
          }
          this.replaces.push(replaces);
        },
        removeReplaces: function (index) {
          this.replaces.splice(index, 1);
        },
        attachNotification: function (notification) {
          this.selectedNotification = null;
          if (this.notifications === undefined) {
            this.notifications = [];
          }
          this.notifications.push(notification);
        },
        removeNotification: function (index) {
          this.notifications.splice(index, 1);
        },
        findDuplicates: function () {
          DomainService.findDomainByName(this.extensions.subAltNames[0]).then(function (domains) { //We should do a better job of searching for multiple domains
            this.duplicates = domains.total;
          });
        },
        useTemplate: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.subAltNames === undefined) {
            this.extensions.subAltNames = {'names': []};
          }

          var saveSubAltNames = this.extensions.subAltNames;
          this.extensions = this.template.extensions;
          this.extensions.subAltNames = saveSubAltNames;
        },
        setEncipherOrDecipher: function (value) {
          if (this.extensions === undefined) {
            this.extensions = {};
          }
          if (this.extensions.keyUsage === undefined) {
            this.extensions.keyUsage = {};
          }
          var existingValue = this.extensions.keyUsage[value];
          if (existingValue) {
            // Clicked on the already-selected value
            this.extensions.keyUsage.useDecipherOnly = false;
            this.extensions.keyUsage.useEncipherOnly = false;
            // Uncheck both radio buttons
            this.encipherOrDecipher = false;
          } else {
            // Clicked a different value
            this.extensions.keyUsage.useKeyAgreement = true;
            if (value === 'useEncipherOnly') {
              this.extensions.keyUsage.useDecipherOnly = false;
              this.extensions.keyUsage.useEncipherOnly = true;
            } else {
              this.extensions.keyUsage.useEncipherOnly = false;
              this.extensions.keyUsage.useDecipherOnly = true;
            }
          }
        },
        setValidityEndDateRange: function (value) {
          // clear selected validity end date as we are about to calculate new range
          this.validityEnd = '';

          // Minimum end date will be same as selected start date
          this.authority.authorityCertificate.minValidityEnd = value;

          if(!this.authority.maxIssuanceDays) {
            this.authority.authorityCertificate.maxValidityEnd = this.authority.authorityCertificate.notAfter;
          } else {
            // Move max end date by maxIssuanceDays
            let endDate = new Date(value);
            endDate.setDate(endDate.getDate() + this.authority.maxIssuanceDays);
            this.authority.authorityCertificate.maxValidityEnd = endDate;
          }
        }
      });
    });
    return LemurRestangular.all('certificates');
  })
  .service('CertificateService', function ($location, CertificateApi, AuthorityService, AuthorityApi, LemurRestangular, DefaultService, DnsProviders) {
    var CertificateService = this;
    CertificateService.findCertificatesByName = function (filterValue) {
      return CertificateApi.getList({'filter[name]': filterValue})
        .then(function (certificates) {
          return certificates;
        });
    };

    CertificateService.create = function (certificate) {
      certificate.attachSubAltName();
      certificate.attachCustom();
      if (certificate.validityYears === '') { // if a user de-selects validity years we ignore it - might not be needed anymore
        delete certificate.validityYears;
      }
      return CertificateApi.post(certificate);
    };

    CertificateService.update = function (certificate) {
      return LemurRestangular.copy(certificate).put();
    };

    CertificateService.upload = function (certificate) {
      return CertificateApi.customPOST(certificate, 'upload');
    };

    CertificateService.getAuthority = function (certificate) {
      return certificate.customGET('authority').then(function (authority) {
        certificate.authority = authority;
      });
    };

    CertificateService.getCreator = function (certificate) {
      return certificate.customGET('creator').then(function (creator) {
        certificate.creator = creator;
      });
    };

    CertificateService.getDestinations = function (certificate) {
      return certificate.getList('destinations').then(function (destinations) {
        certificate.destinations = destinations;
      });
    };

    CertificateService.getNotifications = function (certificate) {
      return certificate.getList('notifications').then(function (notifications) {
        certificate.notifications = notifications;
      });
    };

    CertificateService.getDomains = function (certificate) {
      return certificate.getList('domains').then(function (domains) {
        certificate.domains = domains;
      });
    };

    CertificateService.getReplaces = function (certificate) {
      return certificate.getList('replaces').then(function (replaces) {
        certificate.replaces = replaces;
      });
    };

    CertificateService.getDefaults = function (certificate) {
      return DefaultService.get().then(function (defaults) {
        if (!certificate.country) {
          certificate.country = defaults.country;
        }

        if (!certificate.state) {
          certificate.state = defaults.state;
        }

        if (!certificate.location) {
          certificate.location = defaults.location;
        }

        if (!certificate.organization) {
          certificate.organization = defaults.organization;
        }

        if (!certificate.organizationalUnit) {
          certificate.organizationalUnit = defaults.organizationalUnit;
        }

        if (!certificate.authority) {
          if (!defaults.authority) {
            // set the default authority
            AuthorityApi.getList().then(function(authorities) {
              certificate.authority = authorities[0];
            });
          } else {
            certificate.authority = defaults.authority;
          }
        }

        certificate.authority.authorityCertificate.minValidityEnd = defaults.authority.authorityCertificate.notBefore;
        certificate.authority.authorityCertificate.maxValidityEnd = defaults.authority.authorityCertificate.notAfter;

        // pre-select validity type radio button to default days
        certificate.validityType = 'defaultDays';

        if (certificate.dnsProviderId) {
          certificate.dnsProvider = {id: certificate.dnsProviderId};
        }

        if(!certificate.keyType) {
          certificate.keyType = 'RSA2048'; // default algo to select during clone if backend did not return algo
        }

      });
    };

    CertificateService.getDnsProviders = function () {
      return DnsProviders.get();
    };

    CertificateService.loadPrivateKey = function (certificate) {
      return certificate.customGET('key');
    };

    CertificateService.updateNotify = function (certificate) {
      return certificate.post();
    };

    CertificateService.export = function (certificate) {
      return certificate.customPOST(certificate.exportOptions, 'export');
    };

    CertificateService.revoke = function (certificate) {
      return certificate.customPUT({}, 'revoke');
    };

    return CertificateService;
  });


'use strict';
angular.module('lemur')
  .service('DnsProviderApi', function (LemurRestangular) {
    return LemurRestangular.all('dns_providers');
  })

  .service('DnsProviderOptions', function (LemurRestangular) {
    return LemurRestangular.all('dns_provider_options');
  })

  .service('DnsProviderService', function ($location,  DnsProviderApi, PluginService, DnsProviders, DnsProviderOptions) {
    var DnsProviderService = this;
    DnsProviderService.findDnsProvidersByName = function (filterValue) {
      return DnsProviderApi.getList({'filter[label]': filterValue})
        .then(function (dns_providers) {
          return dns_providers;
        });
    };

    DnsProviderService.getDnsProviders = function () {
      return DnsProviders.get();
    };

    DnsProviderService.getDnsProviderOptions = function () {
      return DnsProviderOptions.getList();
    };

    DnsProviderService.create = function (dns_provider) {
      return DnsProviderApi.post(dns_provider);
    };

    DnsProviderService.get = function () {
      return DnsProviderApi.get();
    };


    DnsProviderService.update = function (dns_provider) {
      return dns_provider.put();
    };

    DnsProviderService.getPlugin = function (dns_provider) {
      return PluginService.getByName(dns_provider.pluginName).then(function (plugin) {
        dns_provider.plugin = plugin;
      });
    };
    return DnsProviderService;
  });

'use strict';
angular.module('lemur')
  .service('DestinationApi', function (LemurRestangular) {
    return LemurRestangular.all('destinations');
  })
  .service('DestinationService', function ($location,  DestinationApi, PluginService) {
    var DestinationService = this;
    DestinationService.findDestinationsByName = function (filterValue) {
      return DestinationApi.getList({'filter[label]': filterValue})
        .then(function (destinations) {
          return destinations;
        });
    };

    DestinationService.create = function (destination) {
      return DestinationApi.post(destination);
    };

    DestinationService.update = function (destination) {
      return destination.put();
    };

    DestinationService.getPlugin = function (destination) {
      return PluginService.getByName(destination.pluginName).then(function (plugin) {
        destination.plugin = plugin;
      });
    };
    return DestinationService;
  });

'use strict';

angular.module('lemur')
  .config(function config($stateProvider) {
    $stateProvider.state('dashboard', {
      url: '/dashboard',
      templateUrl: '/angular/dashboard/dashboard.tpl.html',
      controller: 'DashboardController'
    });
  })
  .controller('DashboardController', function ($scope, $rootScope, $filter, $location, LemurRestangular) {

    $scope.colors = [
      {
        fillColor: 'rgba(41, 171, 224, 0.2)',
        strokeColor: 'rgba(41, 171, 224, 1)',
        pointColor: 'rgba(41, 171, 224, 0.2)',
        pointStrongColor: '#fff',
        pointHighlightFill: '#fff',
        pointHighlightStrokeColor: 'rgba(41, 171, 224, 0.8)'
      }, {
        fillColor: 'rgba(147, 197, 75, 0.2)',
        strokeColor: 'rgba(147, 197, 75, 1)',
        pointColor: 'rgba(147, 197, 75, 0.2)',
        pointStrongColor: '#fff',
        pointHighlightFill: '#fff',
        pointHighlightStrokeColor: 'rgba(147, 197, 75, 0.8)'
      }, {
        fillColor: 'rgba(217, 83, 79, 0.2)',
        strokeColor: 'rgba(217, 83, 79, 1)',
        pointColor: 'rgba(217, 83, 79, 0.2)',
        pointStrongColor: '#fff',
        pointHighlightFill: '#fff',
        pointHighlightStrokeColor: 'rgba(217, 83, 79, 0.8)'
      }, {
        fillColor: 'rgba(244, 124, 60, 0.2)',
        strokeColor: 'rgba(244, 124, 60, 1)',
        pointColor: 'rgba(244, 124, 60, 0.2)',
        pointStrongColor: '#fff',
        pointHighlightFill: '#fff',
        pointHighlightStrokeColor: 'rgba(244, 124, 60, 0.8)'
      }, {
        fillColor: 'rgba(243, 156, 18, 0.2)',
        strokeColor: 'rgba(243, 156, 18, 1)',
        pointColor: 'rgba(243, 156, 18, 0.2)',
        pointStrongColor: '#fff',
        pointHighlightFill: '#fff',
        pointHighlightStrokeColor: 'rgba(243, 156, 18, 0.8)'
      }, {
        fillColor: 'rgba(231, 76, 60, 0.2)',
        strokeColor: 'rgba(231, 76, 60, 1)',
        pointColor: 'rgba(231, 76, 60, 0.2)',
        pointStrongColor: '#fff',
        pointHighlightFill: '#fff',
        pointHighlightStrokeColor: 'rgba(231, 76, 60, 0.8)'
      }, {
        fillColor: 'rgba(255, 102, 102, 0.2)',
        strokeColor: 'rgba(255, 102, 102, 1)',
        pointColor: 'rgba(255, 102, 102, 0.2)',
        pointStrongColor: '#fff',
        pointHighlightFill: '#fff',
        pointHighlightStrokeColor: 'rgba(255, 102, 102, 0.8)'
      }, {
        fillColor: 'rgba(255, 230, 230, 0.2)',
        strokeColor: 'rgba(255, 230, 230, 1)',
        pointColor: 'rgba(255, 230, 230, 0.2)',
        pointStrongColor: '#fff',
        pointHighlightFill: '#fff',
        pointHighlightStrokeColor: 'rgba(255, 230, 230, 0.8)'
      }];

    LemurRestangular.all('certificates').customGET('stats', {metric: 'issuer'})
      .then(function (data) {
        $scope.issuers = data.items;
      });

    LemurRestangular.all('certificates').customGET('stats', {metric: 'bits'})
      .then(function (data) {
        $scope.bits = data.items;
      });

		LemurRestangular.all('certificates').customGET('stats', {metric: 'signing_algorithm'})
			.then(function (data) {
				$scope.algos = data.items;
			});

    LemurRestangular.all('certificates').customGET('stats', {metric: 'not_after'})
      .then(function (data) {
        $scope.expiring = {labels: data.items.labels, values: [data.items.values]};
      });

    LemurRestangular.all('destinations').customGET('stats', {metric: 'certificate'})
      .then(function (data) {
        $scope.destinations = data.items;
      });
  });

'use strict';

angular.module('lemur')
  .service('DomainApi', function (LemurRestangular) {
    return LemurRestangular.all('domains');
  })
  .service('DomainService', function ($location, DomainApi) {
    var DomainService = this;
    DomainService.findDomainByName = function (filterValue) {
      return DomainApi.getList({'filter[name]': filterValue})
        .then(function (domains) {
          return domains;
        });
    };

    DomainService.updateSensitive = function (domain) {
      return domain.put();
    };

    DomainService.create = function (domain) {
      return DomainApi.post(domain);
    };
  });

'use strict';
angular.module('lemur')
  .service('EndpointApi', function (LemurRestangular) {
    return LemurRestangular.all('endpoints');
  })
  .service('EndpointService', function ($location,  EndpointApi) {
    var EndpointService = this;
    EndpointService.findEndpointsByName = function (filterValue) {
      return EndpointApi.getList({'filter[label]': filterValue})
        .then(function (endpoints) {
          return endpoints;
        });
    };

    EndpointService.getCertificates = function (endpoint) {
      endpoint.getList('certificates').then(function (certificates) {
        endpoint.certificates = certificates;
      });
    };
    return EndpointService;
  });

'use strict';

angular.module('lemur')
  .service('LogApi', function (LemurRestangular) {
    return LemurRestangular.all('logs');
  })
  .service('LogService', function () {
    var LogService = this;
    return LogService;
  });

'use strict';
angular.module('lemur')
  .service('NotificationApi', function (LemurRestangular) {
    LemurRestangular.extendModel('notifications', function (obj) {
      return angular.extend(obj, {
        attachCertificate: function (certificate) {
          this.selectedCertificate = null;
          if (this.certificates === undefined) {
            this.certificates = [];
          }
          this.certificates.push(certificate);
        },
        removeCertificate: function (index) {
          this.certificates.splice(index, 1);
        }
      });
    });
    return LemurRestangular.all('notifications');
  })
  .service('NotificationService', function ($location,  NotificationApi, PluginService) {
    var NotificationService = this;
    NotificationService.findNotificationsByName = function (filterValue) {
      return NotificationApi.getList({'filter[label]': filterValue})
        .then(function (notifications) {
          return notifications;
        });
    };

    NotificationService.getCertificates = function (notification) {
      notification.getList('certificates', {showExpired: 0}).then(function (certificates) {
        notification.certificates = certificates;
      });
    };

    NotificationService.getPlugin = function (notification) {
      return PluginService.getByName(notification.pluginName).then(function (plugin) {
        notification.plugin = plugin;
      });
    };


    NotificationService.loadMoreCertificates = function (notification, page) {
      notification.getList('certificates', {page: page, showExpired: 0}).then(function (certificates) {
        _.each(certificates, function (certificate) {
          notification.roles.push(certificate);
        });
      });
    };

    NotificationService.create = function (notification) {
      return NotificationApi.post(notification);
    };

    NotificationService.update = function (notification) {
      return notification.put();
    };

    NotificationService.updateActive = function (notification) {
      notification.put();
    };
    return NotificationService;
  });

'use strict';

angular.module('lemur')
  .service('PluginApi', function (LemurRestangular) {
    return LemurRestangular.all('plugins');
  })
  .service('PluginService', function (PluginApi) {
    var PluginService = this;
    PluginService.get = function () {
      return PluginApi.getList().then(function (plugins) {
        return plugins;
      });
    };

    PluginService.getByType = function (type) {
      return PluginApi.getList({'type': type}).then(function (plugins) {
        return plugins;
      });
    };

    PluginService.getByName = function (pluginName) {
      return PluginApi.customGET(pluginName).then(function (plugin) {
        return plugin;
      });
    };

    return PluginService;
  });

'use strict';

angular.module('lemur')
  .service('PendingCertificateApi', function (LemurRestangular, DomainService) {
    LemurRestangular.extendModel('pending_certificates', function (obj) {
      return angular.extend(obj, {
        attachRole: function (role) {
          this.selectedRole = null;
          if (this.roles === undefined) {
            this.roles = [];
          }
          this.roles.push(role);
        },
        removeRole: function (index) {
          this.roles.splice(index, 1);
        },
        attachAuthority: function (authority) {
          this.authority = authority;
          this.authority.maxDate = moment(this.authority.notAfter).subtract(1, 'days').format('YYYY/MM/DD');
        },
        attachSubAltName: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.subAltNames === undefined) {
            this.extensions.subAltNames = {'names': []};
          }

          if (!angular.isString(this.subAltType)) {
            this.subAltType = 'DNSName';
          }

          if (angular.isString(this.subAltValue) && angular.isString(this.subAltType)) {
            this.extensions.subAltNames.names.push({'nameType': this.subAltType, 'value': this.subAltValue});
            //this.findDuplicates();
          }

          this.subAltType = null;
          this.subAltValue = null;
        },
        removeSubAltName: function (index) {
          this.extensions.subAltNames.names.splice(index, 1);
          //this.findDuplicates();
        },
        attachCustom: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.custom === undefined) {
            this.extensions.custom = [];
          }

          if (angular.isString(this.customOid) && angular.isString(this.customEncoding) && angular.isString(this.customValue)) {
            this.extensions.custom.push(
              {
                'oid': this.customOid,
                'isCritical': this.customIsCritical || false,
                'encoding': this.customEncoding,
                'value': this.customValue
              }
            );
          }

          this.customOid = null;
          this.customIsCritical = null;
          this.customEncoding = null;
          this.customValue = null;
        },
        removeCustom: function (index) {
          this.extensions.custom.splice(index, 1);
        },
        attachDestination: function (destination) {
          this.selectedDestination = null;
          if (this.destinations === undefined) {
            this.destinations = [];
          }
          this.destinations.push(destination);
        },
        removeDestination: function (index) {
          this.destinations.splice(index, 1);
        },
        attachReplaces: function (replaces) {
          this.selectedReplaces = null;
          if (this.replaces === undefined) {
            this.replaces = [];
          }
          this.replaces.push(replaces);
        },
        removeReplaces: function (index) {
          this.replaces.splice(index, 1);
        },
        attachNotification: function (notification) {
          this.selectedNotification = null;
          if (this.notifications === undefined) {
            this.notifications = [];
          }
          this.notifications.push(notification);
        },
        removeNotification: function (index) {
          this.notifications.splice(index, 1);
        },
        findDuplicates: function () {
          DomainService.findDomainByName(this.extensions.subAltNames[0]).then(function (domains) { //We should do a better job of searching for multiple domains
            this.duplicates = domains.total;
          });
        },
        useTemplate: function () {
          if (this.extensions === undefined) {
            this.extensions = {};
          }

          if (this.extensions.subAltNames === undefined) {
            this.extensions.subAltNames = {'names': []};
          }

          var saveSubAltNames = this.extensions.subAltNames;
          this.extensions = this.template.extensions;
          this.extensions.subAltNames = saveSubAltNames;
        },
        setEncipherOrDecipher: function (value) {
          if (this.extensions === undefined) {
            this.extensions = {};
          }
          if (this.extensions.keyUsage === undefined) {
            this.extensions.keyUsage = {};
          }
          var existingValue = this.extensions.keyUsage[value];
          if (existingValue) {
            // Clicked on the already-selected value
            this.extensions.keyUsage.useDecipherOnly = false;
            this.extensions.keyUsage.useEncipherOnly = false;
            // Uncheck both radio buttons
            this.encipherOrDecipher = false;
          } else {
            // Clicked a different value
            this.extensions.keyUsage.useKeyAgreement = true;
            if (value === 'useEncipherOnly') {
              this.extensions.keyUsage.useDecipherOnly = false;
              this.extensions.keyUsage.useEncipherOnly = true;
            } else {
              this.extensions.keyUsage.useEncipherOnly = false;
              this.extensions.keyUsage.useDecipherOnly = true;
            }
          }
        },
        setValidityEndDateRange: function (value) {
          // clear selected validity end date as we are about to calculate new range
          this.validityEnd = '';

          // Minimum end date will be same as selected start date
          this.authority.authorityCertificate.minValidityEnd = value;

          if(!this.authority.maxIssuanceDays) {
            this.authority.authorityCertificate.maxValidityEnd = this.authority.authorityCertificate.notAfter;
          } else {
            // Move max end date by maxIssuanceDays
            let endDate = new Date(value);
            endDate.setDate(endDate.getDate() + this.authority.maxIssuanceDays);
            this.authority.authorityCertificate.maxValidityEnd = endDate;
          }
        }
      });
    });
    return LemurRestangular.all('pending_certificates');
  })
  .service('PendingCertificateService', function ($location, PendingCertificateApi, AuthorityService, AuthorityApi, LemurRestangular, DefaultService) {
    var PendingCertificateService = this;
    PendingCertificateService.findPendingCertificatesByName = function (filterValue) {
      return PendingCertificateApi.getList({'filter[name]': filterValue})
        .then(function (pendingCertificates) {
          return pendingCertificates;
        });
    };

    PendingCertificateService.update = function (pendingCertificate) {
      return LemurRestangular.copy(pendingCertificate).put();
    };

    PendingCertificateService.getAuthority = function (certificate) {
      return certificate.customGET('authority').then(function (authority) {
        certificate.authority = authority;
      });
    };

    PendingCertificateService.getCreator = function (certificate) {
      return certificate.customGET('creator').then(function (creator) {
        certificate.creator = creator;
      });
    };

    PendingCertificateService.getDestinations = function (certificate) {
      return certificate.getList('destinations').then(function (destinations) {
        certificate.destinations = destinations;
      });
    };

    PendingCertificateService.getNotifications = function (certificate) {
      return certificate.getList('notifications').then(function (notifications) {
        certificate.notifications = notifications;
      });
    };

    PendingCertificateService.getDomains = function (certificate) {
      return certificate.getList('domains').then(function (domains) {
        certificate.domains = domains;
      });
    };

    PendingCertificateService.getReplaces = function (certificate) {
      return certificate.getList('replaces').then(function (replaces) {
        certificate.replaces = replaces;
      });
    };

    PendingCertificateService.getDefaults = function (certificate) {
      return DefaultService.get().then(function (defaults) {
        if (!certificate.country) {
          certificate.country = defaults.country;
        }

        if (!certificate.state) {
          certificate.state = defaults.state;
        }

        if (!certificate.location) {
          certificate.location = defaults.location;
        }

        if (!certificate.organization) {
          certificate.organization = defaults.organization;
        }

        if (!certificate.organizationalUnit) {
          certificate.organizationalUnit = defaults.organizationalUnit;
        }

        if (!certificate.authority) {
          if (!defaults.authority) {
            // set the default authority
            AuthorityApi.getList().then(function(authorities) {
              certificate.authority = authorities[0];
            });
          } else {
            certificate.authority = defaults.authority;
          }
        }

        certificate.authority.authorityCertificate.minValidityEnd = defaults.authority.authorityCertificate.notBefore;
        certificate.authority.authorityCertificate.maxValidityEnd = defaults.authority.authorityCertificate.notAfter;
      });
    };

    PendingCertificateService.loadPrivateKey = function (certificate) {
      return certificate.customGET('key');
    };

    PendingCertificateService.updateNotify = function (certificate) {
      return certificate.put();
    };

    PendingCertificateService.cancel = function (pending_certificate, options) {
      return pending_certificate.customOperation('remove', null, {}, {'Content-Type': 'application/json'}, options);
    };

    PendingCertificateService.upload = function (pending_certificate) {
        return pending_certificate.customPOST({'body': pending_certificate.body, 'chain': pending_certificate.chain}, 'upload');
    };

    return PendingCertificateService;
  });

'use strict';
angular.module('lemur')
  .service('SourceApi', function (LemurRestangular) {
    return LemurRestangular.all('sources');
  })
  .service('SourceService', function ($location,  SourceApi, PluginService) {
    var SourceService = this;
    SourceService.findSourcesByName = function (filterValue) {
      return SourceApi.getList({'filter[label]': filterValue})
        .then(function (sources) {
          return sources;
        });
    };

    SourceService.create = function (source) {
      return SourceApi.post(source);
    };

    SourceService.update = function (source) {
      return source.put();
    };

    SourceService.getPlugin = function (source) {
      return PluginService.getByName(source.pluginName).then(function (plugin) {
        source.plugin = plugin;
      });
    };
    return SourceService;
  });

'use strict';

angular.module('lemur')
  .service('RoleApi', function (LemurRestangular) {
    LemurRestangular.extendModel('roles', function (obj) {
      return angular.extend(obj, {
        addUser: function (user) {
          this.selectedUser = null;
          if (this.users === undefined) {
            this.users = [];
          }
          this.users.push(user);
        },
        removeUser: function (index) {
          this.users.splice(index, 1);
        }
      });
    });
    return LemurRestangular.all('roles');
  })
  .service('RoleService', function ($location, RoleApi) {
    var RoleService = this;
    RoleService.findRoleByName = function (filterValue) {
      return RoleApi.getList({'filter[name]': filterValue})
        .then(function (roles) {
          return roles;
        });
    };

    RoleService.getRoleDropDown = function () {
      return RoleApi.getList().then(function (roles) {
        return roles;
      });
    };

    RoleService.getUsers = function (role) {
      return role.getList('users').then(function (users) {
        role.users = users;
      });
    };

    RoleService.loadMoreUsers = function (role, page) {
      role.getList('users', {page: page}).then(function (users) {
        _.each(users, function (user) {
          role.users.push(user);
        });
      });
    };

    RoleService.create = function (role) {
      return RoleApi.post(role);
    };

    RoleService.update = function (role) {
      return role.put();
    };

    RoleService.remove = function (role) {
      return role.remove();
    };

    RoleService.loadPassword = function (role) {
      return role.customGET('credentials');
    };
  });

/**
 * Created by kglisson on 1/19/15.
 */
'use strict';
angular.module('lemur')
  .service('UserApi', function (LemurRestangular, ApiKeyService) {
    LemurRestangular.extendModel('users', function (obj) {
      return angular.extend(obj, {
        attachRole: function (role) {
          this.selectedRole = null;
          if (this.roles === undefined) {
            this.roles = [];
          }
          this.roles.push(role);
        },
        removeRole: function (index) {
          this.roles.splice(index, 1);
        },
        removeApiKey: function (index) {
          var removedApiKeys = this.apiKeys.splice(index, 1);
          var removedApiKey = removedApiKeys[0];
          return ApiKeyService.delete(removedApiKey);
        }
      });
    });
    return LemurRestangular.all('users');
  })
  .service('UserService', function ($location, UserApi, AuthenticationApi) {
    var UserService = this;
    UserService.getCurrentUser = function () {
      return AuthenticationApi.customGET('me').then(function (user) {
        return user;
      });
    };

    UserService.findUserByName = function (filterValue) {
      return UserApi.getList({'filter[username]': filterValue})
        .then(function (users) {
          return users;
        });
    };

    UserService.getRoles = function (user) {
      user.getList('roles').then(function (roles) {
        user.roles = roles;
      });
    };

    UserService.getApiKeys = function (user) {
      user.getList('keys').then(function (apiKeys) {
        user.apiKeys = apiKeys;
      });
    };

    UserService.loadMoreRoles = function (user, page) {
      user.getList('roles', {page: page}).then(function (roles) {
        _.each(roles, function (role) {
          user.roles.push(role);
        });
      });
    };

    UserService.loadMoreApiKeys = function (user, page) {
      user.getList('keys', {page: page}).then(function (apiKeys) {
        _.each(apiKeys, function (apiKey) {
          user.apiKeys.push(apiKey);
        });
      });
    };

    UserService.create = function (user) {
      return UserApi.post(user);
    };

    UserService.update = function (user) {
      return user.put();
    };
  });

'use strict';

angular.module('lemur')
  .controller('ApiKeysCreateController', function ($scope, $uibModalInstance, PluginService, ApiKeyService, UserService, LemurRestangular, toaster) {
    $scope.apiKey = LemurRestangular.restangularizeElement(null, {}, 'keys');

    $scope.origin = window.location.origin;

    $scope.save = function (apiKey) {
      ApiKeyService.create(apiKey).then(
        function (responseBody) {
          toaster.pop({
            type: 'success',
            title: 'Success!',
            body: 'Successfully Created API Token!'
          });
          $scope.jwt = responseBody.jwt;
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: apiKey.name || 'Unnamed API Key',
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.close = function() {
      $uibModalInstance.close();
    };

    $scope.userService = UserService;
  })
  .controller('ApiKeysEditController', function ($scope, $uibModalInstance, ApiKeyService, UserService, LemurRestangular, toaster, editId) {
    LemurRestangular.one('keys', editId).customGET('described').then(function(apiKey) {
      $scope.apiKey = apiKey;
      $scope.selectedUser = apiKey.user;
    });

    $scope.origin = window.location.origin;

    $scope.save = function (apiKey) {
      ApiKeyService.update(apiKey).then(
        function (responseBody) {
          toaster.pop({
            type: 'success',
            title: 'Success',
            body: 'Successfully updated API Token!'
          });
          $scope.jwt = responseBody.jwt;
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: apiKey.name || 'Unnamed API Key',
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.close = function() {
      $uibModalInstance.close();
    };

    $scope.userService = UserService;
  });

'use strict';

angular.module('lemur')
  .config(function config($stateProvider) {
    $stateProvider.state('keys', {
      url: '/keys',
      templateUrl: '/angular/api_keys/view/view.tpl.html',
      controller: 'ApiKeysViewController'
    });
  })
  .controller('ApiKeysViewController', function ($scope, $uibModal, ApiKeyApi, ApiKeyService, ngTableParams, toaster) {
    $scope.filter = {};
    $scope.apiKeysTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        ApiKeyApi.getList(params.url()).then(function (data) {
            params.total(data.total);
            $defer.resolve(data);
          });
      }
    });

    $scope.updateRevoked = function (apiKey) {
      ApiKeyService.update(apiKey).then(
        function () {
          toaster.pop({
            type: 'success',
            title: 'Updated JWT!',
            body: apiKey.jwt
          });
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: apiKey.name || 'Unnamed API Key',
            body: 'Unable to update! ' + response.data.message,
            timeout: 100000
          });
        });
    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'ApiKeysCreateController',
        templateUrl: '/angular/api_keys/api_key/api_key.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.apiKeysTable.reload();
      });

    };

    $scope.remove = function (apiKey) {
      apiKey.remove().then(
        function () {
            toaster.pop({
              type: 'success',
              title: 'Removed!',
              body: 'Deleted that API Key!'
            });
            $scope.apiKeysTable.reload();
          },
          function (response) {
            toaster.pop({
              type: 'error',
              title: 'Opps',
              body: 'I see what you did there: ' + response.data.message
            });
          }
      );
    };

    $scope.edit = function (apiKeyId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/api_keys/api_key/api_key.tpl.html',
        controller: 'ApiKeysEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
            editId: function () {
              return apiKeyId;
            }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.apiKeysTable.reload();
      });

    };

  });

'use strict';

angular.module('lemur')

  .controller('AuthorityEditController', function ($scope, $uibModalInstance, AuthorityApi, AuthorityService, RoleService, toaster, editId){
    AuthorityApi.get(editId).then(function (authority) {
      $scope.authority = authority;
    });

    $scope.roleService = RoleService;

    $scope.save = function (authority) {
      AuthorityService.update(authority).then(
        function () {
          toaster.pop({
            type: 'success',
            title: authority.name,
            body: 'Successfully updated!'
          });
          $uibModalInstance.close();
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: authority.name,
            body: 'Update Failed! ' + response.data.message,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  })

  .controller('AuthorityCreateController', function ($scope, $uibModalInstance, AuthorityService, AuthorityApi, LemurRestangular, RoleService, PluginService, WizardHandler, toaster, DestinationService)  {
    $scope.authority = LemurRestangular.restangularizeElement(null, {}, 'authorities');
    // set the defaults
    AuthorityService.getDefaults($scope.authority).then(function () {
      PluginService.getByType('issuer').then(function (plugins) {
          $scope.plugins = plugins;
          if ($scope.authority.defaultIssuerPlugin) {
            plugins.forEach(function(plugin) {
              if (plugin.slug === $scope.authority.defaultIssuerPlugin) {
                $scope.authority.plugin = plugin;
              }
            });
          } else {
            $scope.authority.plugin = plugins[0];
          }
      });
    });

    $scope.getDestinations = function() {
      return DestinationService.findDestinationsByName('').then(function(destinations) {
        $scope.destinations = destinations;
      });
    };

    $scope.getAuthoritiesByName = function (value) {
      return AuthorityService.findAuthorityByName(value).then(function (authorities) {
        $scope.authorities = authorities;
      });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.create = function (authority) {
      WizardHandler.wizard().context.loading = true;
      AuthorityService.create(authority).then(
				function () {
          toaster.pop({
            type: 'success',
            title: authority.name,
            body: 'Was created!'
          });
					$uibModalInstance.close();
				},
				function (response) {
					toaster.pop({
						type: 'error',
						title: authority.name,
						body: 'Was not created! ' + response.data.message,
            timeout: 100000
					});
          WizardHandler.wizard().context.loading = false;
      });
    };

    $scope.roleService = RoleService;
    $scope.authorityService = AuthorityService;

    $scope.dateOptions = {
      formatYear: 'yy',
      maxDate: new Date(2020, 5, 22),
      minDate: new Date(),
      startingDay: 1
    };

    $scope.clearDates = function () {
      $scope.authority.validityStart = null;
      $scope.authority.validityEnd = null;
      $scope.authority.validityYears = null;
    };

    $scope.open1 = function() {
      $scope.popup1.opened = true;
    };

    $scope.open2 = function() {
      $scope.popup2.opened = true;
    };

    $scope.setDate = function(year, month, day) {
      $scope.dt = new Date(year, month, day);
    };

    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[0];
    $scope.altInputFormats = ['M!/d!/yyyy'];

    $scope.popup1 = {
      opened: false
    };

    $scope.popup2 = {
      opened: false
    };

    $scope.populateSubjectEmail = function () {
      $scope.authority.email = $scope.authority.owner;
    };

  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider
      .state('authorities', {
        url: '/authorities',
        templateUrl: '/angular/authorities/view/view.tpl.html',
        controller: 'AuthoritiesViewController'
      })
      .state('authority', {
        url: '/authorities/:name',
        templateUrl: '/angular/authorities/view/view.tpl.html',
        controller: 'AuthoritiesViewController'
      });
  })

  .directive('authorityVisualization', function () {
    // constants
    var margin = {top: 20, right: 120, bottom: 20, left: 120},
    width = 960 - margin.right - margin.left,
    height = 400 - margin.top - margin.bottom;

    return {
      restrict: 'E',
      scope: {
        val: '=',
        grouped: '='
      },
      link: function (scope, element) {
        function update(source) {

          // Compute the new tree layout.
          var nodes = tree.nodes(root).reverse(),
            links = tree.links(nodes);

          // Normalize for fixed-depth.
          nodes.forEach(function(d) { d.y = d.depth * 180; });

          // Update the nodes…
          var node = svg.selectAll('g.node')
            .data(nodes, function(d) { return d.id || (d.id = ++i); });

          // Enter any new nodes at the parent's previous position.
          var nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr('transform', function() { return 'translate(' + source.y0 + ',' + source.x0 + ')'; })
            .on('click', click);

          nodeEnter.append('circle')
            .attr('r', 1e-6)
            .style('fill', function(d) { return d._children ? 'lightsteelblue' : '#fff'; });

          nodeEnter.append('text')
            .attr('x', function(d) { return d.children || d._children ? -10 : 10; })
            .attr('dy', '.35em')
            .attr('text-anchor', function(d) { return d.children || d._children ? 'end' : 'start'; })
            .text(function(d) { return d.name; })
            .style('fill-opacity', 1e-6);

          // Transition nodes to their new position.
          var nodeUpdate = node.transition()
            .duration(duration)
            .attr('transform', function(d) { return 'translate(' + d.y + ',' + d.x + ')'; });

          nodeUpdate.select('circle')
            .attr('r', 4.5)
            .style('fill', function(d) { return d._children ? 'lightsteelblue' : '#fff'; });

          nodeUpdate.select('text')
            .style('fill-opacity', 1);

          // Transition exiting nodes to the parent's new position.
          var nodeExit = node.exit().transition()
            .duration(duration)
            .attr('transform', function() { return 'translate(' + source.y + ',' + source.x + ')'; })
            .remove();

          nodeExit.select('circle')
            .attr('r', 1e-6);

          nodeExit.select('text')
            .style('fill-opacity', 1e-6);

          // Update the links…
          var link = svg.selectAll('path.link')
            .data(links, function(d) { return d.target.id; });

          // Enter any new links at the parent's previous position.
          link.enter().insert('path', 'g')
            .attr('class', 'link')
            .attr('d', function() {
              var o = {x: source.x0, y: source.y0};
              return diagonal({source: o, target: o});
            });

          // Transition links to their new position.
          link.transition()
            .duration(duration)
            .attr('d', diagonal);

          // Transition exiting nodes to the parent's new position.
          link.exit().transition()
            .duration(duration)
            .attr('d', function() {
              var o = {x: source.x, y: source.y};
              return diagonal({source: o, target: o});
            })
            .remove();

          // Stash the old positions for transition.
          nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
          });
        }

        // Toggle children on click.
        function click(d) {
          if (d.children) {
            d._children = d.children;
            d.children = null;
          } else {
            d.children = d._children;
            d._children = null;
          }
          update(d);
        }

        var i = 0,
            duration = 750,
            root;

        var tree = d3.layout.tree()
            .size([height, width]);

        var diagonal = d3.svg.diagonal()
            .projection(function(d) { return [d.y, d.x]; });

        var svg = d3.select(element[0]).append('svg')
            .attr('width', width + margin.right + margin.left)
            .attr('height', height + margin.top + margin.bottom)
            .call(d3.behavior.zoom().on('zoom', function () {
              svg.attr('transform', 'translate(' + d3.event.translate + ')' + ' scale(' + d3.event.scale + ')');
            }))
            .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        scope.val.customGET('visualize').then(function (result) {
          root = result;
          root.x0 = height / 2;
          root.y0 = 0;

          function collapse(d) {
            if (d.children) {
              d._children = d.children;
              d._children.forEach(collapse);
              d.children = null;
            }
          }

          root.children.forEach(collapse);
          update(root);

        });

        d3.select(self.frameElement).style('height', '800px');

      }
    };
  })

  .controller('AuthoritiesViewController', function ($scope, $q, $uibModal, $stateParams, AuthorityApi, AuthorityService, MomentService, ngTableParams, toaster) {
    $scope.filter = $stateParams;
    $scope.authoritiesTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        AuthorityApi.getList(params.url()).then(function (data) {
          params.total(data.total);
          $defer.resolve(data);
        });
      }
    });

    $scope.momentService = MomentService;

    $scope.updateActive = function (authority) {
      AuthorityService.updateActive(authority).then(
				function () {
					toaster.pop({
						type: 'success',
						title: authority.name,
						body: 'Successfully updated!'
					});
				},
				function (response) {
					toaster.pop({
						type: 'error',
						title: authority.name,
						body: 'Update Failed! ' + response.data.message,
            timeout: 100000
					});
				});
    };

    $scope.getAuthorityStatus = function () {
      var def = $q.defer();
      def.resolve([{'title': 'Active', 'id': true}, {'title': 'Inactive', 'id': false}]);
      return def;
    };

    $scope.edit = function (authorityId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/authorities/authority/edit.tpl.html',
        controller: 'AuthorityEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return authorityId;
          }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.authoritiesTable.reload();
      });

    };

    $scope.editRole = function (roleId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/roles/role/role.tpl.html',
        controller: 'RolesEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return roleId;
          }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.authoritiesTable.reload();
      });

    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'AuthorityCreateController',
        templateUrl: '/angular/authorities/authority/authorityWizard.tpl.html',
        size: 'lg',
        backdrop: 'static',
      });

      uibModalInstance.result.then(function () {
        $scope.authoritiesTable.reload();
      });

    };
  });

'use strict';

angular.module('lemur')
  .config(function config($stateProvider) {
    $stateProvider.state('logout', {
      controller: 'LogoutCtrl',
      url: '/logout'
    });
  })
  .controller('LogoutCtrl', function ($scope, $location, lemurRestangular, userService) {
    userService.logout();
    $location.path('/');
  });

'use strict';

angular.module('lemur')
  .config(function config($stateProvider) {
    $stateProvider.state('login', {
      url: '/login',
      templateUrl: '/angular/authentication/login/login.tpl.html',
      controller: 'LoginController',
      params: {
        'toState': 'certificates',
        'toParams': {}
      }
    });
  })
  .controller('LoginController', function ($rootScope, $scope, $state, $auth, AuthenticationService, UserService, providers, toaster) {
    $scope.login = function (username, password) {
      return AuthenticationService.login(username, password).then(
        function (user) {
          $auth.setToken(user.token, true);
          $rootScope.$emit('user:login');
          $state.go($state.params.toState, $state.params.toParams);
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: 'Whoa there',
            body: response.data.message,
            showCloseButton: true
          });
        });
    };

    $scope.authenticate = function (provider) {
      return AuthenticationService.authenticate(provider).then(
        function (user) {
          $auth.setToken(user.token, true);
          $rootScope.$emit('user:login');
          $state.go($state.params.toState, $state.params.toParams);
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: 'Whoa there',
            body: response.data.message,
            showCloseButton: true
          });
        });
    };

    $scope.logout = AuthenticationService.logout;

    $scope.providers = providers;

    UserService.getCurrentUser().then(function (user) {
      $scope.currentUser = user;
    });

    $rootScope.$on('user:login', function () {
      UserService.getCurrentUser().then(function (user) {
        $scope.currentUser = user;
      });
    });

    $rootScope.$on('user:logout', function () {
      $scope.currentUser = null;
    });
  });
'use strict';

angular.module('lemur')
  .controller('CertificateExportController', function ($scope, $uibModalInstance, CertificateApi, CertificateService, PluginService, FileSaver, Blob, toaster, editId) {
    CertificateApi.get(editId).then(function (certificate) {
      $scope.certificate = certificate;
    });

    PluginService.getByType('export').then(function (plugins) {
      $scope.plugins = plugins;
    });

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.save = function (certificate) {
      CertificateService.export(certificate).then(
        function (response) {
            var byteCharacters = atob(response.data);
            var byteArrays = [];

            for (var offset = 0; offset < byteCharacters.length; offset += 512) {
              var slice = byteCharacters.slice(offset, offset + 512);

              var byteNumbers = new Array(slice.length);
              for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
              }

              var byteArray = new Uint8Array(byteNumbers);

              byteArrays.push(byteArray);
            }

          var blob = new Blob(byteArrays, {type: 'application/octet-stream'});
          FileSaver.saveAs(blob, certificate.name + '.' + response.extension);
          $scope.passphrase = response.passphrase;
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: certificate.name,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };
  })
  .controller('CertificateEditController', function ($scope, $uibModalInstance, CertificateApi, CertificateService, DestinationService, NotificationService, toaster, editId) {
    CertificateApi.get(editId).then(function (certificate) {
      $scope.certificate = certificate;
    });

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.save = function (certificate) {
      CertificateService.update(certificate).then(
        function () {
          toaster.pop({
            type: 'success',
            title: certificate.name,
            body: 'Successfully updated!'
          });
          $uibModalInstance.close();
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: certificate.name,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.certificateService = CertificateService;
    $scope.destinationService = DestinationService;
    $scope.notificationService = NotificationService;
  })

  .controller('CertificateCreateController', function ($scope, $uibModalInstance, CertificateApi, CertificateService, DestinationService, AuthorityService, AuthorityApi, PluginService, MomentService, WizardHandler, LemurRestangular, NotificationService, toaster) {
    $scope.certificate = LemurRestangular.restangularizeElement(null, {}, 'certificates');
    // set the defaults
    CertificateService.getDefaults($scope.certificate);

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.getAuthoritiesByName = function (value) {
      return AuthorityService.findActiveAuthorityByName(value).then(function (authorities) {
        $scope.authorities = authorities;
      });
    };

    $scope.dateOptions = {
      formatYear: 'yy',
      maxDate: new Date(2020, 5, 22),
      minDate: new Date(),
      startingDay: 1
    };

    $scope.open1 = function() {
      $scope.popup1.opened = true;
    };

    $scope.open2 = function() {
      $scope.popup2.opened = true;
    };

    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[0];
    $scope.altInputFormats = ['M!/d!/yyyy'];

    $scope.popup1 = {
      opened: false
    };

    $scope.popup2 = {
      opened: false
    };

    $scope.clearDates = function () {
      $scope.certificate.validityStart = null;
      $scope.certificate.validityEnd = null;
      $scope.certificate.validityYears = null;
    };

    CertificateService.getDnsProviders().then(function (providers) {
            $scope.dnsProviders = providers;
        }
    );

    $scope.create = function (certificate) {
      if(certificate.validityType === 'customDates' &&
          (!certificate.validityStart || !certificate.validityEnd)) { // these are not mandatory fields in schema, thus handling validation in js
          return showMissingDateError();
      }
      if(certificate.validityType === 'defaultDays') {
        populateValidityDateAsPerDefault(certificate);
      }

      WizardHandler.wizard().context.loading = true;
      CertificateService.create(certificate).then(
        function () {
          toaster.pop({
            type: 'success',
            title: certificate.name,
            body: 'Successfully created!'
          });
          $uibModalInstance.close();
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: certificate.name,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });

          WizardHandler.wizard().context.loading = false;
        });
    };

    function showMissingDateError() {
      let error = {};
      error.message = '';
      error.reasons = {};
      error.reasons.validityRange = 'Valid start and end dates are needed, else select Default option';

      toaster.pop({
        type: 'error',
        title: 'Validation Error',
        body: 'lemur-bad-request',
        bodyOutputType: 'directive',
        directiveData: error,
        timeout: 100000
      });
    }

    function populateValidityDateAsPerDefault(certificate) {
      // calculate start and end date as per default validity
      let startDate = new Date(), endDate = new Date();
      endDate.setDate(startDate.getDate() + certificate.authority.defaultValidityDays);
      certificate.validityStart = startDate;
      certificate.validityEnd = endDate;
    }

    $scope.templates = [
      {
        'name': 'Client Certificate',
        'description': '',
        'extensions': {
          'basicConstraints': {},
          'keyUsage': {
            'useDigitalSignature': true
          },
          'extendedKeyUsage': {
            'useClientAuthentication': true
          },
          'subjectKeyIdentifier': {
            'includeSKI': true
          }
        }
      },
      {
        'name': 'Server Certificate',
        'description': '',
        'extensions' : {
          'basicConstraints': {},
          'keyUsage': {
            'useKeyEncipherment': true,
            'useDigitalSignature': true
          },
          'extendedKeyUsage': {
            'useServerAuthentication': true
          },
          'subjectKeyIdentifier': {
            'includeSKI': true
          }
        }
      }
    ];


    PluginService.getByType('destination').then(function (plugins) {
        $scope.plugins = plugins;
    });

    $scope.certificateService = CertificateService;
    $scope.authorityService = AuthorityService;
    $scope.destinationService = DestinationService;
    $scope.notificationService = NotificationService;
  })

.controller('CertificateCloneController', function ($scope, $uibModalInstance, CertificateApi, CertificateService, DestinationService, AuthorityService, AuthorityApi, PluginService, MomentService, WizardHandler, LemurRestangular, NotificationService, toaster, editId) {
  $scope.certificate = LemurRestangular.restangularizeElement(null, {}, 'certificates');
  CertificateApi.get(editId).then(function (certificate) {
    $scope.certificate = certificate;
    // prepare the certificate for cloning
    $scope.certificate.name = ''; // we should prefer the generated name
    $scope.certificate.csr = null;  // should not clone CSR in case other settings are changed in clone
    $scope.certificate.validityStart = null;
    $scope.certificate.validityEnd = null;
    $scope.certificate.description = 'Cloning from cert ID ' + editId;
    $scope.certificate.replacedBy = []; // should not clone 'replaced by' info
    $scope.certificate.removeReplaces(); // should not clone 'replacement cert' info

    CertificateService.getDefaults($scope.certificate);
  });

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };

  $scope.getAuthoritiesByName = function (value) {
    return AuthorityService.findAuthorityByName(value).then(function (authorities) {
      $scope.authorities = authorities;
    });
  };

  $scope.dateOptions = {
    formatYear: 'yy',
    maxDate: new Date(2020, 5, 22),
    minDate: new Date(),
    startingDay: 1
  };


  $scope.open1 = function() {
    $scope.popup1.opened = true;
  };

  $scope.open2 = function() {
    $scope.popup2.opened = true;
  };

  $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
  $scope.format = $scope.formats[0];
  $scope.altInputFormats = ['M!/d!/yyyy'];

  $scope.popup1 = {
    opened: false
  };

  $scope.popup2 = {
    opened: false
  };

  CertificateService.getDnsProviders().then(function (providers) {
            $scope.dnsProviders = providers;
        }
    );

  $scope.clearDates = function () {
    $scope.certificate.validityStart = null;
    $scope.certificate.validityEnd = null;
    $scope.certificate.validityYears = null;
  };

  $scope.create = function (certificate) {
     if(certificate.validityType === 'customDates' &&
          (!certificate.validityStart || !certificate.validityEnd)) { // these are not mandatory fields in schema, thus handling validation in js
          return showMissingDateError();
     }
     if(certificate.validityType === 'defaultDays') {
        populateValidityDateAsPerDefault(certificate);
     }

    WizardHandler.wizard().context.loading = true;
    CertificateService.create(certificate).then(
      function () {
        toaster.pop({
          type: 'success',
          title: certificate.name,
          body: 'Successfully created!'
        });
        $uibModalInstance.close();
      },
      function (response) {
        toaster.pop({
          type: 'error',
          title: certificate.name,
          body: 'lemur-bad-request',
          bodyOutputType: 'directive',
          directiveData: response.data,
          timeout: 100000
        });

        WizardHandler.wizard().context.loading = false;
      });
  };

  function showMissingDateError() {
      let error = {};
      error.message = '';
      error.reasons = {};
      error.reasons.validityRange = 'Valid start and end dates are needed, else select Default option';

      toaster.pop({
        type: 'error',
        title: 'Validation Error',
        body: 'lemur-bad-request',
        bodyOutputType: 'directive',
        directiveData: error,
        timeout: 100000
      });
    }

    function populateValidityDateAsPerDefault(certificate) {
      // calculate start and end date as per default validity
      let startDate = new Date(), endDate = new Date();
      endDate.setDate(startDate.getDate() + certificate.authority.defaultValidityDays);
      certificate.validityStart = startDate;
      certificate.validityEnd = endDate;
    }

  $scope.templates = [
    {
      'name': 'Client Certificate',
      'description': '',
      'extensions': {
        'basicConstraints': {},
        'keyUsage': {
          'useDigitalSignature': true
        },
        'extendedKeyUsage': {
          'useClientAuthentication': true
        },
        'subjectKeyIdentifier': {
          'includeSKI': true
        }
      }
    },
    {
      'name': 'Server Certificate',
      'description': '',
      'extensions' : {
        'basicConstraints': {},
        'keyUsage': {
          'useKeyEncipherment': true,
          'useDigitalSignature': true
        },
        'extendedKeyUsage': {
          'useServerAuthentication': true
        },
        'subjectKeyIdentifier': {
          'includeSKI': true
        }
      }
    }
  ];

  PluginService.getByType('destination').then(function (plugins) {
    $scope.plugins = plugins;
  });

  $scope.certificateService = CertificateService;
  $scope.authorityService = AuthorityService;
  $scope.destinationService = DestinationService;
  $scope.notificationService = NotificationService;
})

.controller('CertificateRevokeController', function ($scope, $uibModalInstance, CertificateApi, CertificateService, LemurRestangular, NotificationService, toaster, revokeId) {
  CertificateApi.get(revokeId).then(function (certificate) {
    $scope.certificate = certificate;
  });

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };

  $scope.revoke = function (certificate) {
   CertificateService.revoke(certificate).then(
      function () {
        toaster.pop({
          type: 'success',
          title: certificate.name,
          body: 'Successfully revoked!'
        });
        $uibModalInstance.close();
      },
      function (response) {
        toaster.pop({
          type: 'error',
          title: certificate.name,
          body: 'lemur-bad-request',
          bodyOutputType: 'directive',
          directiveData: response.data,
          timeout: 100000
        });
      });
  };
})
.controller('CertificateInfoController', function ($scope, CertificateApi) {
  $scope.fetchFullCertificate = function (certId) {
    CertificateApi.get(certId).then(function (certificate) {
      $scope.certificate = certificate;
    });
  };
})
;

'use strict';

angular.module('lemur')

  .controller('CertificateUploadController', function ($scope, $uibModalInstance, CertificateService, LemurRestangular, DestinationService, NotificationService, PluginService, toaster) {
    $scope.certificate = LemurRestangular.restangularizeElement(null, {}, 'certificates');
    $scope.upload = CertificateService.upload;

    $scope.destinationService = DestinationService;
    $scope.notificationService = NotificationService;
    $scope.certificateService = CertificateService;

    PluginService.getByType('destination').then(function (plugins) {
        $scope.plugins = plugins;
    });

    $scope.save = function (certificate) {
      CertificateService.upload(certificate).then(
        function () {
          toaster.pop({
            type: 'success',
            title: certificate.name,
            body: 'Successfully uploaded!'
          });
          $uibModalInstance.close();
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: certificate.name,
            body: 'Failed to upload ' + response.data.message,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {

    $stateProvider
      .state('certificates', {
        url: '/certificates',
        templateUrl: '/angular/certificates/view/view.tpl.html',
        controller: 'CertificatesViewController'
      })
      .state('certificate', {
        url: '/certificates/:fixedName', // use "fixedName" if in URL to indicate 'like' query can be avoided
        templateUrl: '/angular/certificates/view/view.tpl.html',
        controller: 'CertificatesViewController'
      });
  })

  .controller('CertificatesViewController', function ($q, $scope, $uibModal, $stateParams, CertificateApi, CertificateService, MomentService, ngTableParams, toaster) {
    $scope.filter = $stateParams;
    $scope.expiredText = ['Show Expired', 'Hide Expired'];
    $scope.expiredValue = 0;
    $scope.expiredButton = $scope.expiredText[$scope.expiredValue];
    $scope.certificateTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      short: true,
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        CertificateApi.getList(params.url())
          .then(function (data) {
            params.total(data.total);
            $defer.resolve(data);
          });
      }
    });

    $scope.showExpired = function () {
      if ($scope.expiredValue === 0) {
        $scope.expiredValue = 1;
      }
      else {
        $scope.expiredValue = 0;
      }
      $scope.expiredButton = $scope.expiredText[$scope.expiredValue];
      $scope.certificateTable = new ngTableParams({
        page: 1,            // show first page
        count: 10,          // count per page
        sorting: {
          id: 'desc'     // initial sorting
        },
        short: true,
        filter: $scope.filter
      }, {
        getData: function ($defer, params) {
          $scope.temp = angular.copy(params.url());
          $scope.temp.showExpired = $scope.expiredValue;
          CertificateApi.getList($scope.temp)
            .then(function (data) {
              params.total(data.total);
              $defer.resolve(data);
            });
        }
      });
    };

    $scope.momentService = MomentService;

    $scope.remove = function (certificate) {
      certificate.remove().then(
        function () {
          $scope.certificateTable.reload();
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: certificate.name,
            body: 'Unable to remove certificate! ' + response.data.message,
            timeout: 100000
          });
        });
    };

    $scope.loadPrivateKey = function (certificate) {
      if (certificate.privateKey !== undefined) {
        return;
      }

      CertificateService.loadPrivateKey(certificate).then(
        function (response) {
          if (response.key === null) {
            toaster.pop({
              type: 'warning',
              title: certificate.name,
              body: 'No private key found!'
            });
          } else {
            certificate.privateKey = response.key;
          }
        },
        function () {
          toaster.pop({
            type: 'error',
            title: certificate.name,
            body: 'You do not have permission to view this key!',
            timeout: 100000
          });
        });
    };

    $scope.updateNotify = function (certificate) {
      CertificateService.updateNotify(certificate).then(
        function () {
          toaster.pop({
            type: 'success',
            title: certificate.name,
            body: 'Updated!'
          });
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: certificate.name,
            body: 'Unable to update! ' + response.data.message,
            timeout: 100000
          });
          certificate.notify = false;
        });
    };
    $scope.getCertificateStatus = function () {
      var def = $q.defer();
      def.resolve([{'title': 'True', 'id': true}, {'title': 'False', 'id': false}]);
      return def;
    };

    $scope.show = {title: 'Current User', value: 'currentUser'};

    $scope.fields = [{title: 'Current User', value: 'currentUser'}, {title: 'All', value: 'all'}];

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'CertificateCreateController',
        templateUrl: '/angular/certificates/certificate/certificateWizard.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.certificateTable.reload();
      });
    };

    $scope.clone = function (certificateId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'CertificateCloneController',
        templateUrl: '/angular/certificates/certificate/certificateWizard.tpl.html',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return certificateId;
          }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.certificateTable.reload();
      });
    };

    $scope.edit = function (certificateId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'CertificateEditController',
        templateUrl: '/angular/certificates/certificate/edit.tpl.html',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return certificateId;
          }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.certificateTable.reload();
      });
    };

    $scope.import = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'CertificateUploadController',
        templateUrl: '/angular/certificates/certificate/upload.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.certificateTable.reload();
      });
    };

    $scope.export = function (certificateId) {
      $uibModal.open({
        animation: true,
        controller: 'CertificateExportController',
        templateUrl: '/angular/certificates/certificate/export.tpl.html',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return certificateId;
          }
        }
      });
    };

     $scope.revoke = function (certificateId) {
      $uibModal.open({
        animation: true,
        controller: 'CertificateRevokeController',
        templateUrl: '/angular/certificates/certificate/revoke.tpl.html',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          revokeId: function () {
            return certificateId;
          }
        }
      });
    };
  });

'use strict';

angular.module('lemur')

  .controller('DnsProviderCreateController', function ($scope, $uibModalInstance, PluginService, DnsProviderService, LemurRestangular, toaster) {
    $scope.dns_provider = LemurRestangular.restangularizeElement(null, {}, 'dns_providers');

    DnsProviderService.getDnsProviderOptions().then(function(res) {
        $scope.options = res;
    });

    $scope.save = function (dns_provider) {
      DnsProviderService.create(dns_provider).then(
        function () {
          toaster.pop({
            type: 'success',
            title: dns_provider.label,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: dns_provider.label,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  })

  .controller('DnsProviderEditController', function ($scope, $uibModalInstance, DnsProviderService, DnsProviderApi, PluginService, toaster, editId) {
    DnsProviderService.getDnsProviderOptions().then(function(res) {
      $scope.options = res;
    });

    DnsProviderApi.get(editId).then(function (dns_provider) {
      $scope.dns_provider = dns_provider;
    });

    $scope.save = function (dns_provider) {
      DnsProviderService.update(dns_provider).then(
        function () {
          toaster.pop({
            type: 'success',
            title: dns_provider.label,
            body: 'Successfully Updated!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: dns_provider.label,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('dns_providers', {
      url: '/dns_providers',
      templateUrl: '/angular/dns_providers/view/view.tpl.html',
      controller: 'DnsProvidersViewController'
    });
  })

  .controller('DnsProvidersViewController', function ($scope, $uibModal, DnsProviderApi, DnsProviderService, ngTableParams, toaster) {
    $scope.filter = {};
    $scope.dnsProvidersTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        DnsProviderApi.getList(params.url()).then(
          function (data) {
            params.total(data.total);
            $defer.resolve(data);
          }
        );
      }
    });

    $scope.remove = function (dns_provider) {
      dns_provider.remove().then(
        function () {
            $scope.dnsProvidersTable.reload();
          },
          function (response) {
            toaster.pop({
              type: 'error',
              title: 'Opps',
              body: 'I see what you did there: ' + response.data.message
            });
          }
      );
    };

    $scope.edit = function (dns_providerId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/dns_providers/dns_provider/dns_provider.tpl.html',
        controller: 'DnsProviderEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
            editId: function () {
              return dns_providerId;
            }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.dnsProvidersTable.reload();
      });

    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'DnsProviderCreateController',
        templateUrl: '/angular/dns_providers/dns_provider/dns_provider.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.dnsProvidersTable.reload();
      });

    };

  });

'use strict';

angular.module('lemur')

  .controller('DestinationsCreateController', function ($scope, $uibModalInstance, PluginService, DestinationService, LemurRestangular, toaster) {
    $scope.destination = LemurRestangular.restangularizeElement(null, {}, 'destinations');

    PluginService.getByType('destination').then(function (plugins) {
      $scope.plugins = plugins;
    });

    PluginService.getByType('export').then(function (plugins) {
      $scope.exportPlugins = plugins;
    });

    $scope.save = function (destination) {
      DestinationService.create(destination).then(
        function () {
          toaster.pop({
            type: 'success',
            title: destination.label,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: destination.label,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  })

  .controller('DestinationsEditController', function ($scope, $uibModalInstance, DestinationService, DestinationApi, PluginService, toaster, editId) {


    DestinationApi.get(editId).then(function (destination) {
      $scope.destination = destination;

      PluginService.getByType('destination').then(function (plugins) {
        $scope.plugins = plugins;

        _.each($scope.plugins, function (plugin) {
          if (plugin.slug === $scope.destination.plugin.slug) {
            plugin.pluginOptions = $scope.destination.plugin.pluginOptions;
            $scope.destination.plugin = plugin;
            PluginService.getByType('export').then(function (plugins) {
              $scope.exportPlugins = plugins;

              _.each($scope.destination.plugin.pluginOptions, function (option) {
                if (option.type === 'export-plugin') {
                  _.each($scope.exportPlugins, function (plugin) {
                    if (plugin.slug === option.value.slug) {
                      plugin.pluginOptions = option.value.pluginOptions;
                      option.value = plugin;
                    }
                  });
                }
              });
            });
          }
        });
      });
    });

    $scope.save = function (destination) {
      DestinationService.update(destination).then(
        function () {
          toaster.pop({
            type: 'success',
            title: destination.label,
            body: 'Successfully Updated!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: destination.label,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('destinations', {
      url: '/destinations',
      templateUrl: '/angular/destinations/view/view.tpl.html',
      controller: 'DestinationsViewController'
    });
  })

  .controller('DestinationsViewController', function ($scope, $uibModal, DestinationApi, DestinationService, ngTableParams, toaster) {
    $scope.filter = {};
    $scope.destinationsTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        DestinationApi.getList(params.url()).then(
          function (data) {
            params.total(data.total);
            $defer.resolve(data);
          }
        );
      }
    });

    $scope.remove = function (destination) {
      destination.remove().then(
        function () {
            $scope.destinationsTable.reload();
          },
          function (response) {
            toaster.pop({
              type: 'error',
              title: 'Opps',
              body: 'I see what you did there: ' + response.data.message
            });
          }
      );
    };

    $scope.edit = function (destinationId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/destinations/destination/destination.tpl.html',
        controller: 'DestinationsEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
            editId: function () {
              return destinationId;
            }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.destinationsTable.reload();
      });

    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'DestinationsCreateController',
        templateUrl: '/angular/destinations/destination/destination.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.destinationsTable.reload();
      });

    };

  });

'use strict';

angular.module('lemur')

  .controller('DomainsCreateController', function ($scope, $uibModalInstance, PluginService, DomainService, LemurRestangular, toaster){
    $scope.domain = LemurRestangular.restangularizeElement(null, {}, 'domains');

    $scope.save = function (domain) {
      DomainService.create(domain).then(
        function () {
          toaster.pop({
            type: 'success',
            title: domain.name,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: domain,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  })

  .controller('DomainsEditController', function ($scope, $uibModalInstance, DomainService, DomainApi, toaster, editId) {
    DomainApi.get(editId).then(function (domain) {
      $scope.domain = domain;
    });

    $scope.save = function (domain) {
      DomainService.update(domain).then(
        function () {
          toaster.pop({
            type: 'success',
            title: domain,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: domain,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('domains', {
      url: '/domains',
      templateUrl: '/angular/domains/view/view.tpl.html',
      controller: 'DomainsViewController'
    });
  })

  .controller('DomainsViewController', function ($scope, $uibModal, DomainApi, DomainService, ngTableParams, toaster) {
    $scope.filter = {};
    $scope.domainsTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        DomainApi.getList(params.url()).then(function (data) {
            params.total(data.total);
            $defer.resolve(data);
          });
      }
    });

    $scope.updateSensitive = function (domain) {
      DomainService.updateSensitive(domain).then(
        function () {
          toaster.pop({
            type: 'success',
            title: domain.name,
            body: 'Updated!'
          });
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: domain.name,
            body: 'Unable to update! ' + response.data.message,
            timeout: 100000
          });
          domain.sensitive = !domain.sensitive;
        });
    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'DomainsCreateController',
        templateUrl: '/angular/domains/domain/domain.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.domainsTable.reload();
      });

    };

  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('endpoints', {
      url: '/endpoints',
      templateUrl: '/angular/endpoints/view/view.tpl.html',
      controller: 'EndpointsViewController'
    });
  })

  .controller('EndpointsViewController', function ($q, $scope, $uibModal, EndpointApi, EndpointService, MomentService, ngTableParams) {
    $scope.filter = {};
    $scope.endpointsTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        EndpointApi.getList(params.url()).then(
          function (data) {
            params.total(data.total);
            $defer.resolve(data);
          }
        );
      }
    });


    $scope.ciphers = [
      {'title': 'Protocol-SSLv2', 'id': 'Protocol-SSLv2'},
      {'title': 'Protocol-SSLv3', 'id': 'Protocol-SSLv3'},
      {'title': 'Protocol-TLSv1', 'id': 'Protocol-TLSv1'},
      {'title': 'Protocol-TLSv1.1', 'id': 'Protocol-TLSv1.1'},
      {'title': 'Protocol-TLSv1.2', 'id': 'Protocol-TLSv1.2'},
    ];

    $scope.momentService = MomentService;

    $scope.endpointService = EndpointService;

  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('logs', {
      url: '/logs',
      templateUrl: '/angular/logs/view/view.tpl.html',
      controller: 'LogsViewController'
    });
  })

  .controller('LogsViewController', function ($scope, $uibModal, LogApi, LogService, ngTableParams, MomentService) {
    $scope.filter = {};
    $scope.logsTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        LogApi.getList(params.url()).then(function (data) {
            params.total(data.total);
            $defer.resolve(data);
          });
      }
    });

    $scope.momentService = MomentService;
  });

'use strict';

angular.module('lemur')

  .controller('NotificationsCreateController', function ($scope, $uibModalInstance, PluginService, NotificationService, CertificateService, LemurRestangular, toaster){
    $scope.notification = LemurRestangular.restangularizeElement(null, {}, 'notifications');

    PluginService.getByType('notification').then(function (plugins) {
      $scope.plugins = plugins;
    });
    $scope.save = function (notification) {
      NotificationService.create(notification).then(
        function () {
          toaster.pop({
            type: 'success',
            title: notification.label,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: notification.label,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.certificateService = CertificateService;
  })

  .controller('NotificationsEditController', function ($scope, $uibModalInstance, NotificationService, NotificationApi, PluginService, CertificateService, toaster, editId) {
    NotificationApi.get(editId).then(function (notification) {
      $scope.notification = notification;
      PluginService.getByType('notification').then(function (plugins) {
        $scope.plugins = plugins;
        _.each($scope.plugins, function (plugin) {
          if (plugin.slug === $scope.notification.plugin.slug) {
            plugin.pluginOptions = $scope.notification.plugin.pluginOptions;
            $scope.notification.plugin = plugin;
          }
        });
      });
      NotificationService.getCertificates(notification);
    });

    $scope.save = function (notification) {
      NotificationService.update(notification).then(
        function () {
          toaster.pop({
            type: 'success',
            title: notification.label,
            body: 'Successfully Updated!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: notification.label,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.certificateService = CertificateService;
  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('notifications', {
      url: '/notifications',
      templateUrl: '/angular/notifications/view/view.tpl.html',
      controller: 'NotificationsViewController'
    });
  })

  .controller('NotificationsViewController', function ($q, $scope, $uibModal, NotificationApi, NotificationService, ngTableParams, toaster) {
    $scope.filter = {};
    $scope.notificationsTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        NotificationApi.getList(params.url()).then(
          function (data) {
            params.total(data.total);
            $defer.resolve(data);
          }
        );
      }
    });

    $scope.getNotificationStatus = function () {
      var def = $q.defer();
      def.resolve([{'title': 'Active', 'id': true}, {'title': 'Inactive', 'id': false}]);
      return def;
    };

    $scope.remove = function (notification) {
      notification.remove().then(
        function () {
          $scope.notificationsTable.reload();
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: 'Opps',
            body: 'I see what you did there: ' + response.data.message
          });
        }
      );
    };

    $scope.edit = function (notificationId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/notifications/notification/notification.tpl.html',
        controller: 'NotificationsEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return notificationId;
          }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.notificationsTable.reload();
      });

    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'NotificationsCreateController',
        templateUrl: '/angular/notifications/notification/notification.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.notificationsTable.reload();
      });

    };

    $scope.notificationService = NotificationService;

  });

'use strict';

angular.module('lemur')
.controller('PendingCertificateEditController', function ($scope, $uibModalInstance, PendingCertificateApi, PendingCertificateService, CertificateService, DestinationService, NotificationService, toaster, editId) {
  PendingCertificateApi.get(editId).then(function (pendingCertificate) {
    $scope.pendingCertificate = pendingCertificate;
  });

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };

  $scope.save = function (pendingCertificate) {
    PendingCertificateService.update(pendingCertificate).then(
      function () {
        toaster.pop({
          type: 'success',
          title: pendingCertificate.name,
          body: 'Successfully updated!'
        });
        $uibModalInstance.close();
      },
      function (response) {
        toaster.pop({
          type: 'error',
          title: pendingCertificate.name,
          body: 'lemur-bad-request',
          bodyOutputType: 'directive',
          directiveData: response.data,
          timeout: 100000
        });
      });
  };

  $scope.pendingCertificateService = PendingCertificateService;
  $scope.certificateService = CertificateService;
  $scope.destinationService = DestinationService;
  $scope.notificationService = NotificationService;
})
.controller('PendingCertificateCancelController', function ($scope, $uibModalInstance, PendingCertificateApi, PendingCertificateService, toaster, cancelId) {
  PendingCertificateApi.get(cancelId).then(function (pendingCertificate) {
    $scope.pendingCertificate = pendingCertificate;
  });

  $scope.exit = function () {
    $uibModalInstance.dismiss('cancel');
  };

  $scope.cancel = function (pendingCertificate, cancelOptions) {
    PendingCertificateService.cancel(pendingCertificate, cancelOptions).then(
      function () {
        toaster.pop({
          type: 'success',
          title: pendingCertificate.name,
          body: 'Successfully cancelled pending certificate!'
        });
        $uibModalInstance.close();
      },
      function (response) {
        toaster.pop({
          type: 'error',
          title: pendingCertificate.name,
          body: 'lemur-bad-request',
          bodyOutputType: 'directive',
          directiveData: response.data,
          timeout: 100000
        });
      });
  };


});

'use strict';

angular.module('lemur')
    .controller('PendingCertificateUploadController', function ($scope, $uibModalInstance, PendingCertificateApi, PendingCertificateService, toaster, uploadId) {
    PendingCertificateApi.get(uploadId).then(function (pendingCertificate) {
      $scope.pendingCertificate = pendingCertificate;
    });

    $scope.upload = PendingCertificateService.upload;
    $scope.save = function (pendingCertificate) {
      PendingCertificateService.upload(pendingCertificate).then(
        function () {
          toaster.pop({
            type: 'success',
            title: pendingCertificate.name,
            body: 'Successfully uploaded!'
          });
          $uibModalInstance.close();
        },
        function (response) {
          toaster.pop({
            type: 'error',
            title: pendingCertificate.name,
            body: 'Failed to upload ' + response.data.message,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider
      .state('pending_certificates', {
        url: '/pending_certificates',
        templateUrl: '/angular/pending_certificates/view/view.tpl.html',
        controller: 'PendingCertificatesViewController'
      })
      .state('pending_certificate', {
        url: '/pending_certificates/:name',
        templateUrl: '/angular/pending_certificates/view/view.tpl.html',
        controller: 'PendingCertificatesViewController'
      });
  })

  .controller('PendingCertificatesViewController', function ($q, $scope, $uibModal, $stateParams, PendingCertificateApi, PendingCertificateService, ngTableParams, toaster) {
    $scope.filter = $stateParams;
    $scope.pendingCertificateTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        PendingCertificateApi.getList(params.url())
          .then(function (data) {
            params.total(data.total);
            $defer.resolve(data);
          });
      }
    });

    $scope.edit = function (pendingCertificateId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'PendingCertificateEditController',
        templateUrl: '/angular/pending_certificates/pending_certificate/edit.tpl.html',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return pendingCertificateId;
          }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.pendingCertificateTable.reload();
      });
    };

    $scope.loadPrivateKey = function (pendingCertificate) {
      if (pendingCertificate.privateKey !== undefined) {
        return;
      }

      PendingCertificateService.loadPrivateKey(pendingCertificate).then(
        function (response) {
          if (response.key === null) {
            toaster.pop({
              type: 'warning',
              title: pendingCertificate.name,
              body: 'No private key found!'
            });
          } else {
            pendingCertificate.privateKey = response.key;
          }
        },
        function () {
          toaster.pop({
            type: 'error',
            title: pendingCertificate.name,
            body: 'You do not have permission to view this key!',
            timeout: 100000
          });
        });
    };

    $scope.cancel = function (pendingCertificateId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'PendingCertificateCancelController',
        templateUrl: '/angular/pending_certificates/pending_certificate/cancel.tpl.html',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          cancelId: function () {
            return pendingCertificateId;
          }
        }
      });
      uibModalInstance.result.then(function () {
        $scope.pendingCertificateTable.reload();
      });
    };

    $scope.upload = function (pendingCertificateId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'PendingCertificateUploadController',
        templateUrl: '/angular/pending_certificates/pending_certificate/upload.tpl.html',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          uploadId: function () {
            return pendingCertificateId;
          }
        }
      });
      uibModalInstance.result.then(function () {
        $scope.pendingCertificateTable.reload();
      });
    };

  });

'use strict';

angular.module('lemur')

  .controller('SourcesCreateController', function ($scope, $uibModalInstance, PluginService, SourceService, LemurRestangular, toaster){
    $scope.source = LemurRestangular.restangularizeElement(null, {}, 'sources');

    PluginService.getByType('source').then(function (plugins) {
        $scope.plugins = plugins;
    });

    $scope.save = function (source) {
      SourceService.create(source).then(
        function () {
          toaster.pop({
            type: 'success',
            title: source.label,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: source.label,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  })

  .controller('SourcesEditController', function ($scope, $uibModalInstance, SourceService, SourceApi, PluginService, toaster, editId) {
    SourceApi.get(editId).then(function (source) {
      $scope.source = source;
      PluginService.getByType('source').then(function (plugins) {
        $scope.plugins = plugins;
        _.each($scope.plugins, function (plugin) {
          if (plugin.slug === $scope.source.plugin.slug) {
            plugin.pluginOptions = $scope.source.plugin.pluginOptions;
            $scope.source.plugin = plugin;
          }
        });
      });
    });

    $scope.save = function (source) {
      SourceService.update(source).then(
        function () {
          toaster.pop({
            type: 'success',
            title: source.label,
            body: 'Successfully Updated!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: source.label,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
      });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('sources', {
      url: '/sources',
      templateUrl: '/angular/sources/view/view.tpl.html',
      controller: 'SourcesViewController'
    });
  })

  .controller('SourcesViewController', function ($scope, $uibModal, SourceApi, SourceService, ngTableParams, toaster) {
    $scope.filter = {};
    $scope.sourcesTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        SourceApi.getList(params.url()).then(
          function (data) {
            params.total(data.total);
            $defer.resolve(data);
          }
        );
      }
    });

    $scope.remove = function (source) {
      source.remove().then(
        function () {
            $scope.sourcesTable.reload();
          },
          function (response) {
            toaster.pop({
              type: 'error',
              title: 'Opps',
              body: 'I see what you did there: ' + response.data.message
            });
          }
      );
    };

    $scope.edit = function (sourceId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/sources/source/source.tpl.html',
        controller: 'SourcesEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
            editId: function () {
              return sourceId;
            }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.sourcesTable.reload();
      });

    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'SourcesCreateController',
        templateUrl: '/angular/sources/source/source.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.sourcesTable.reload();
      });

    };

  });

'use strict';

angular.module('lemur')
.directive('roleSelect', function (RoleApi) {
    return {
      restrict: 'AE',
      scope: {
        ngModel: '='
      },
      replace: true,
      require: 'ngModel',
      templateUrl: '/angular/roles/role/roleSelect.tpl.html',
      link: function postLink($scope) {
        RoleApi.getList().then(function (roles) {
          $scope.roles = roles;
        });

        $scope.findRoleByName = function (search) {
          return RoleApi.getList({'filter[name]': search})
            .then(function (roles) {
              return roles;
            });
        };
      }
    };
  })
  .controller('RolesEditController', function ($scope, $uibModalInstance, RoleApi, RoleService, UserService, toaster, editId) {
    RoleApi.get(editId).then(function (role) {
      $scope.role = role;
    });

    $scope.save = function (role) {
      RoleService.update(role).then(
        function () {
          toaster.pop({
            type: 'success',
            title: role.name,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: role.name,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
      });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.userPage = 1;
    $scope.loadMoreRoles = function () {
      $scope.userPage += 1;
      RoleService.loadMoreUsers($scope.role, $scope.userPage);
    };

    $scope.userService = UserService;

    $scope.loadPassword = function (role) {
      RoleService.loadPassword(role).then(
        function (response) {
          $scope.role.password = response.password;
          $scope.role.username = response.username;
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: role.name,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };
  })

  .controller('RolesCreateController', function ($scope,$uibModalInstance, RoleApi, RoleService, UserService, LemurRestangular, toaster) {
    $scope.role = LemurRestangular.restangularizeElement(null, {}, 'roles');
    $scope.userService = UserService;

    $scope.save = function (role) {
      RoleService.create(role).then(
       function () {
          toaster.pop({
            type: 'success',
            title: role.name,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: role.name,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('roles', {
      url: '/roles',
      templateUrl: '/angular/roles/view/view.tpl.html',
      controller: 'RolesViewController'
    });
  })

  .controller('RolesViewController', function ($scope, $uibModal, RoleApi, RoleService, ngTableParams) {
    $scope.filter = {};
    $scope.rolesTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        RoleApi.getList(params.url())
          .then(function (data) {
            params.total(data.total);
            $defer.resolve(data);
          });
      }
    });

    $scope.remove = function (role) {
      RoleService.remove(role).then(function () {
        $scope.rolesTable.reload();
      });
    };

    $scope.edit = function (roleId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/roles/role/role.tpl.html',
        controller: 'RolesEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return roleId;
          }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.rolesTable.reload();
      });

    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'RolesCreateController',
        templateUrl: '/angular/roles/role/role.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.rolesTable.reload();
      });

    };

  });

'use strict';

angular.module('lemur')

  .controller('UsersEditController', function ($scope, $uibModalInstance, UserApi, UserService, RoleService, ApiKeyService, toaster, editId) {
    UserApi.get(editId).then(function (user) {
      $scope.user = user;
      UserService.getApiKeys(user);
    });

    $scope.roleService = RoleService;
    $scope.apiKeyService = ApiKeyService;

    $scope.rolePage = 1;
    $scope.apiKeyPage = 1;

    $scope.save = function (user) {
      UserService.update(user).then(
        function () {
          toaster.pop({
            type: 'success',
            title: user.username,
            body: 'Successfully Updated!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: user.username,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    $scope.removeApiKey = function (idx) {
      UserApi.removeApiKey(idx).then(function () {
        toaster.pop({
          type: 'success',
          title: 'Removed API Key!',
          body: 'Successfully removed the api key!'
        });
      }, function(err) {
        toaster.pop({
          type: 'error',
          title: 'Failed to remove API Key!',
          body: 'lemur-bad-request',
          bodyOutputType: 'directive',
          directiveData: err,
          timeout: 100000
        });
      });
    };

    $scope.loadMoreRoles = function () {
      $scope.rolePage += 1;
      UserService.loadMoreRoles($scope.user, $scope.rolePage);
    };

    $scope.loadMoreApiKeys = function () {
      $scope.apiKeyPage += 1;
      UserService.loadMoreApiKeys($scope.user, $scope.apiKeyPage);
    };
  })

  .controller('UsersCreateController', function ($scope, $uibModalInstance, UserService, LemurRestangular, RoleService, ApiKeyService, toaster) {
    $scope.user = LemurRestangular.restangularizeElement(null, {}, 'users');
    $scope.roleService = RoleService;
    $scope.apiKeyService = ApiKeyService;

    $scope.save = function (user) {
      UserService.create(user).then(
        function () {
          toaster.pop({
            type: 'success',
            title: user.username,
            body: 'Successfully Created!'
          });
          $uibModalInstance.close();
        }, function (response) {
          toaster.pop({
            type: 'error',
            title: user.username,
            body: 'lemur-bad-request',
            bodyOutputType: 'directive',
            directiveData: response.data,
            timeout: 100000
          });
        });
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

  });

'use strict';

angular.module('lemur')

  .config(function config($stateProvider) {
    $stateProvider.state('users', {
      url: '/users',
      templateUrl: '/angular/users/view/view.tpl.html',
      controller: 'UsersViewController'
    });
  })

  .controller('UsersViewController', function ($scope, $uibModal, UserApi, UserService, ngTableParams) {
    $scope.filter = {};
    $scope.usersTable = new ngTableParams({
      page: 1,            // show first page
      count: 10,          // count per page
      sorting: {
        id: 'desc'     // initial sorting
      },
      filter: $scope.filter
    }, {
      total: 0,           // length of data
      getData: function ($defer, params) {
        UserApi.getList(params.url()).then(
          function (data) {
              params.total(data.total);
              $defer.resolve(data);
          }
        );
      }
    });

    $scope.remove = function (account) {
      account.remove().then(function () {
        $scope.usersTable.reload();
      });
    };

    $scope.edit = function (userId) {
      var uibModalInstance = $uibModal.open({
        animation: true,
        templateUrl: '/angular/users/user/user.tpl.html',
        controller: 'UsersEditController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          editId: function () {
            return userId;
          }
        }
      });

      uibModalInstance.result.then(function () {
        $scope.usersTable.reload();
      });

    };

    $scope.create = function () {
      var uibModalInstance = $uibModal.open({
        animation: true,
        controller: 'UsersCreateController',
        templateUrl: '/angular/users/user/user.tpl.html',
        size: 'lg',
        backdrop: 'static'
      });

      uibModalInstance.result.then(function () {
        $scope.usersTable.reload();
      });

    };

  });
