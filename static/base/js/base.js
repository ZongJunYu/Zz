$(function () {
    // 为了将滚动条隐藏
    // 假设屏幕320 + 20（滚动条的大小）
    $('#content').width(innerWidth+20)

    document.documentElement.style.fontSize = innerWidth / 320 * 16 + 'px'
})