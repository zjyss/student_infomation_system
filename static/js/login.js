$(function () {
    $('#sub').click(function (event) {
        event.preventDefault();
        var school_id = $('#student_school_id').val();
        var passwd = $('#student_passwd').val();
        alert(school_id)
        if (school_id !== '' && passwd !== ''){
            $.post(
            '/index/',
            {
                'student_school_id':school_id,
                'student_passwd':passwd,
            },
            function (data) {
                if (data['code'] === '200'){
                    // 直接带上用户id请求接口信息，在信息页面接受返回的data
                    //用vue来进行渲染
                    //保存id
                    alert(data['id']);
                    sessionStorage.setItem('id',data['id']);
                    window.location.href = 'log_in/'
                }
            }
        )
        }

    })
});