import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('code', function() {
    this.route('curriculum');
    this.route('duration');
    this.route('jobs');
    this.route('offering');
    this.route('schedule');
  });
  this.route('cost');
  this.route('rent', function() {
    this.route('you', {
    });
    this.route('me', {
    });
    this.route('cost', {
    });
    this.route('house');
    this.route('offering');
  });
  this.route('email');
});

export default Router;
