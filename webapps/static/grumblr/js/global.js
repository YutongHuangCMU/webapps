function populateList() {
    $.get("get-posts-global")
      .done(function(data) {
          var list = $("#post-list");
          list.data('max-time', data['max-time']);
          list.html('');
          for (var i = 0; i < data.posts.length; i++) {
              var post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              list.append(new_post);
              $.get("get-comments-global-post/"+post.id)
                .done(function(data) {
                  var com_name="#com-list-"+data['post_id'];
                  var list_com = $(com_name);
                  list_com.data('max-time', data['max-time']);
                  for (var i = 0; i < data.comments.length; i++) {
                      var comment = data.comments[i];
                      var new_comment = $(comment.html);
                      new_comment.data("comment-id", comment.id);
                      list_com.append(new_comment);
                    }
                });
          }
      });
}

function addPost(){
  var post = $("#txt-post");
    $.post("add-post-global", {post: post.val()})
      .done(function(data) {
          getUpdates();
          post.val("").focus();
      });
}

function addComment(e){
  console.log($(e.target).parent());
  var id = $(e.target).parent().data("post-id");
  var text_id = "#text-com-" + id;
  var txt = $(text_id);
  $.post("comment-global/"+id, {comment: txt.val()})
    .done(function(data) {
        getUpdateComment(id);
        txt.val("");
        txt.focus();
    });
}

function getUpdateComment(id){
  var com_id = "#com-list-" + id;
  var list = $(com_id);
  var max_time = list.data("max-time");
//  $.get("get-comments/"+ max_time)
  $.get("get-comments-global-post/" + id + "/" + max_time )
    .done(function(data) {
      list.data('max-time', data['max-time']);
      for (var i = 0; i < data.comments.length; i++) {
        var comment = data.comments[i];
        var new_comment = $(comment.html);
        new_comment.data("comment-id", comment.id);
        list.append(new_comment);
        }
    });
}

function getUpdates() {
  var list = $("#post-list")
  var max_time = list.data("max-time")
  $.get("get-posts-global/"+ max_time)
    .done(function(data) {
      list.data('max-time', data['max-time']);
      for (var i = 0; i < data.posts.length; i++) {
        var post = data.posts[i];
        var new_post = $(post.html);
        new_post.data("post-id", post.id);
        list.prepend(new_post);
        var com_name="#com-list-" +post.id;
        var list_com = $(com_name);
        list_com.data('max-time', post.max_comment_time);
        list_com.html('');
        console.log(list_com.data("max-time"));
      }
    });
}

$(document).ready(function () {
  if($('body').is('.afterlogin')){
  populateList();
  $("#post-field").focus();
  $("#btn-post").click(addPost);
  $("#post-list").click(function(e) {
    if ( $(e.target).is( "button" ) ) {
      addComment(e);
    }
  });

  // Periodically refresh post
  window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs

}
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
