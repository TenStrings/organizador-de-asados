$(function () {
   $.validator.methods.date = function (value, element) {
       return this.optional(element) || moment(value, 'DD/MM/YYYY').isValid() || moment(value, 'h:mm a').isValid();
 };
});

$(function () {
   $.validator.methods.datetime = function (value, element) {
       return this.optional(element) || moment(value, 'h:mm a').isValid();
 };
});
