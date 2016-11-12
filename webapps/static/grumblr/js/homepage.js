function populateList(url) {
    $.get("get-posts-homepage/"+url)
      .done(function(data) {
          var list = $("#post-list");
          list.data('max-time', data['max-time']);
          list.html('');
          for (var i = 0; i < data.posts.length; i++) {
              var post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              list.append(new_post);
              console.log(post.id);
              $.get("get-comments-global-post/"+post.id)
                .done(function(data) {
                  console.log(data);
                  var com_name="#com-list-"+data['post_id'];
                  var list_com = $(com_name);
                  list_com.data('max-time', data['max-time']);
                  console.log(com_name);
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

function addComment(e){
  console.log($(e.target).parent());
  var id = $(e.target).parent().data("post-id");
  var text_id = "#text-com-" + id;
  var txt = $(text_id);
  $.post("comment-global/"+id, {comment: txt.val()})
    .done(function(data) {
        getUpdateComment(id);
        $("#post-field").val("").focus()
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


$(document).ready(function () {
  if($('body').is('.afterlogin')){
    var url = window.location.pathname;
    url = url.substring(10);
    console.log(url);
  populateList(url);
  $("#post-list").click(function(e) {
    if ( $(e.target).is( "button" ) ) {
      addComment(e);
    }
  });

  // Periodically refresh post
}
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
