$(function () {
    $('#log_out').click(function (event) {
        event.preventDefault();
        var id = sessionStorage.getItem('id');
        $.post(
            '/logout/',
            {
                'id':id
            },
            function (data) {
                if (data['code']==='200'){
                    sessionStorage.clear();
                    window.location.href = '/'
                }else {
                    alert('退出失败')
                }
            }
        );

    })
})