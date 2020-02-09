
function OnSubmitFooter(token) {
  document.getElementById("footerNewsLetter").submit();
}
function OnSubmitCustom(token) {
  document.getElementById("customNewsLetter").submit();
}




$(function() {
  $('.matchHeight').matchHeight();
  $('.matchHeight_header').matchHeight();
  $('.matchHeight_title').matchHeight();
  $('.matchHeight_specsHeader').matchHeight();
  $('.matchHeight_pricingHeader').matchHeight();


  $('.matchHeight_specs').matchHeight();

  $('.matchHeight_card').matchHeight();

});
