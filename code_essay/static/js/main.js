function toggle_item($trigger_target_list) {
  $trigger_target_list.map($item =>
    $item[0].on('click touch', function() {
      $trigger_target_list.map($subitem => {
        if ($subitem !== $item && $subitem[1] && $subitem[2]) {
          $subitem[1].hide();
          $subitem[0].removeClass('article__menu-item--checked');
        }
      });
      if ($item[1]) {
        $item[1].toggle();
        if ($item[0].hasClass('article__menu-item--checked')) {$item[0].removeClass('article__menu-item--checked');} else {$item[0].addClass('article__menu-item--checked');}
      }
    }));
}


$(function() {

  toggle_item([
    [$('#js-article__menu--code'), $('#js-article__edit'), false],
    [$('#js-article__menu--comment'), $('#js-article__comment'), true],
    [$('#js-article__menu--others'), $('#js-article__others-menu'), true],
    [$('#js-user__menu--others'), $('#js-user__others-menu'), true],
    [$('#js-header__menu-icon'), $('#js-search'), true],
  ]);

  // --- Markdown, MathJax 関連 ---
  // marked 設定
  marked.setOptions({
    gfm: true,
    tables: true,
    breaks: false,
    pedantic: false,
    sanitize: true,
    smartLists: true,
    smartypants: false,
    langPrefix: 'language-',
  });

});
