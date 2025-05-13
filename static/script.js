$(document).ready(function () {
  $("#chat-form").on("submit", function (e) {
    e.preventDefault();
    const input = $("#user-input");
    const message = input.val().trim();
    if (!message) return;

    const userMessageHtml = `<div class="message user-message">${message}</div>`;
    $("#chat-body").append(userMessageHtml);
    input.val("");

    $.post("/get", { msg: message }, function (data) {
      const botMessageHtml = `<div class="message bot-message">${data}</div>`;
      $("#chat-body").append(botMessageHtml);
      $("#chat-body").scrollTop($("#chat-body")[0].scrollHeight);
    });
  });
});
