function successCallback(token) {
  htmx.trigger("#captcha-form", "captcha-completed");
  console.log(token);
}
