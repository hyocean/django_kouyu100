layui.use('element', function () {
    var element = layui.element; //导航的hover效果、二级菜单等功能，需要依赖element模块

    // 监听导航点击
    element.on('nav(test)', function (elem) {
        element.tabAdd('demo', {
            title: elem.find('span').text()
            , content: '<span>hahahhah</span>' //支持传入html
        })
    });
});
