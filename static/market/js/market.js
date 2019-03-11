$(function () {
    /* jquery.cookie用法

    设置
    $.cookie(value,key,arg)

    获取
    value=$.cookie(key)

    删除
    $.cookie(key,null)
     */
    // var index=localStorage.getItem('index')
    var index = $.cookie('index')
    console.log(index)
    if (index) {
        $('.type-slider li').eq(index).addClass('active')
    } else {
        $('.type-slider li:first').addClass('active')
    }


    //側邊欄（分類）點擊
    //问题：点击效果是可以的，但是因a标签的原因，点击后会刷新重新加载页面，导致样式又刷新
    $('.type-slider li').click(function () {
        //$(this)当前点击的对象
        // $(this).addClass('active')


        //解决 点击后 记录下来
        // localStorage.setItem('index',$(this).index())
        $.cookie('index', $(this).index(), {expires: 3, path: '/'})
    })


     // 子类
    var categoryShow = false
    $('#category-bt').click(function () {
        // console.log(categoryShow)
        // if (categoryShow){  // 隐藏
        //     categoryShow = false
        //     $('.category-view').hide()
        // } else { // 显示
        //     categoryShow = true
        //     $('.category-view').show()
        // }

        // 取反
        categoryShow = !categoryShow
        categoryShow ? categoryViewShow() : categoryViewHide()

        console.log('子类点击')
    })

    function categoryViewShow() {
        $('.category-view').show()
        $('#category-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        sortViewHide()
        sortShow = false
    }

    function categoryViewHide() {
        $('.category-view').hide()
        $('#category-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }

    // 排序
    var sortShow = false
    $('#sort-bt').click(function () {
        sortShow = !sortShow
        sortShow ? sortViewShow() : sortViewHide()

        console.log('排序点击')
    })

    function sortViewShow() {
        $('.sort-view').show()
        $('#sort-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        categoryViewHide()
        categoryShow = false
    }

    function sortViewHide() {
        $('.sort-view').hide()
        $('#sort-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }

    //灰色
    $('.bounce-view').click(function () {
        categoryViewHide()
        categoryShow = false
        sortViewHide()
        sortShow = false
    })


    //隐藏处理
    $('.bt-wrapper>.glyphicon-minus').hide()
    $('.bt-wrapper>i').hide()


    $('.bt-wrapper>.glyphicon-plus').click(function () {


        //参数：用户user.商品goods
        //user因为状态保持，所以可以不传.
        console.log('1')

        response_data={

        }

        $('/axf/addcart',response_data,function (response) {
            console.log(response)
            if(response.status==-1){
                window.open('/axf/login','_self')
            }

        })
    })

})



