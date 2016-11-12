function populateList() {
    $.get("get-posts")
      .done(function(data) {
          var list = $("#post-list");
          list.data('max-time', data['max-time']);
          list.html('')
          for (var i = 0; i < data.posts.length; i++) {
              item = data.posts[i];
              var new_item = $(post.html);
              new_post.data("post-id", post.id);
              list.append(new_post);
          }
      });
}

function addPost(){
    var txtPost = $("#txt-post");
    $.post("post-global", {post: txtPost.val()})
      .done(function(data) {
          getUpdates();
          txtPost.val("").focus();
      });
}

function getUpdates(){
  var list = $("#post-list")
    var max_time = list.data("max-time")
    $.get("post-global")
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            var new_post = $(post.html);
            new_post.data("item-id", post.id);
            list.append(new_post);
          }
      });
}


$(document).ready(function () {
  // Add event-handlers
  //$("#btn-com").click(addComment);
  $("#btn-post").click(addPost);

  // Set up to-do list with initial DB items and DOM data
  populateList();
  $("#item-field").focus();

  // Periodically refresh post
  window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
