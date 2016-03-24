import Ember from 'ember';

export default Ember.Controller.extend({
  isAddButtonDisabled: Ember.computed('newEmail', 'yourEmail', function() {
    var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (Ember.isEmpty(this.get('newEmail'))) {
      return true
    } else {
      return !re.test(this.get('yourEmail'));
    }
  })
});
