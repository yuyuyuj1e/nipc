(
    function ($) {
        'use strict';
        // 紧凑侧边栏模式和水平菜单模式下悬停时打开子菜单
        $ (document).on ('mouseenter mouseleave', '.sidebar .nav-item', function (ev) {
            var body = $ ('body');
            var sidebarIconOnly = body.hasClass ("sidebar-icon-only");
            var sidebarFixed = body.hasClass ("sidebar-fixed");
            if (!(
                'ontouchstart' in document.documentElement
            )) {
                if (sidebarIconOnly) {
                    if (sidebarFixed) {
                        if (ev.type === 'mouseenter') {
                            body.removeClass (`sidebar-icon-only`);
                        }
                    }
                    else {
                        var $menuItem = $ (this);
                        if (ev.type === 'mouseenter') {
                            $menuItem.addClass ('hover-open')
                        }
                        else {
                            $menuItem.removeClass ('hover-open')
                        }
                    }
                }
            }
        });
    }
) (jQuery);