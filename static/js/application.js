/* Timer function for alerts */
window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 4000);

/* form clear button */
$('.has-clear input[type="text"]').on('input propertychange', function() {
    var $this = $(this);
    var visible = Boolean($this.val());
    $this.siblings('.form-control-clear').toggleClass('hidden', !visible);
  }).trigger('propertychange');
  
  $('.form-control-clear').click(function() {
    $(this).siblings('input[type="text"]').val('')
      .trigger('propertychange').focus();
  });