function dispLineNumber($textarea) {
  var $linenumber = $('#js-article__line-number-wrap').find('#js-article__line-number');
  if (!$linenumber.length) {
    var $linenumber_box = $("<div class='article__line-number-wrap' id='js-article__line-number-wrap'><ul class='article__line-number' id='js-article__line-number'></ul></div>");
    $linenumber_box.insertAfter($textarea);
    $linenumber = $linenumber_box.find('#js-article__line-number');
  }
  var split_line = $textarea.val().match(/\n|\r\n/g);
  var line_num = split_line ? split_line.length : 0;
  var num_list = "";
  $linenumber.html("");
  for (let i = 1; i < line_num + 2; i++) {
    num_list += '<li>' + i + '</li>'
  }
  $linenumber.html(num_list);
}

function scrollLineNumber($textarea) {
  var scrolled = $textarea.scrollTop();
  var $linenumber = $('#js-article__line-number-wrap').find('#js-article__line-number');
  $linenumber.scrollTop(scrolled);
}

function updateView($textarea, $view) {
  var code = marked($textarea.val());
  $view.html(code);
  MathJax.Hub.Queue(["Typeset", MathJax.Hub, "preview"]);
}

$(function () {

  var $edit_box = $('#js-article__textarea');
  var $view_box = $('#js-article__view');

  if (!$edit_box.val()) {
    $edit_box.val($view_box.text());
    updateView($edit_box, $view_box);
    dispLineNumber($edit_box);
  }

  $edit_box.on('focus', function () {
    dispLineNumber($(this));
  }).on('input', function () {
    dispLineNumber($(this));
    updateView($(this), $view_box);
    scrollLineNumber($(this));
  }).on('scroll', function () {
    scrollLineNumber($(this));
  });

});
