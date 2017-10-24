$(document).ready(function() {
  $("#id_organizer").change(function(){
    $('#id_attendee option').each(function(){
      $(this).show();
    });
    var organizerName = $(this).find("option:selected").text();
    $('#id_attendee option[value=' + organizerName + ']').hide();
  })
});
