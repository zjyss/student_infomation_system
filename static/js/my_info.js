let vm = new Vue({
    el: '#content',
    data: {
        infolist: '',
    },
    methods: {
        getinfo: function () {
            var id = sessionStorage.getItem('id');
            $.post(
                '/my_info/',
                {
                    'id': id
                },
                function (data) {
                    vm.infolist = data['info'];
                    console.log(vm.infolist)
                }
            )
        }
    },
    mounted() {
        this.getinfo();
    }
});

$(function () {
    $('#btn').click(function (event) {
        event.preventDefault();
        var id = sessionStorage.getItem('id');
        var tel = $('#student_tel').val();
        var email = $('#student_email').val();
        var addr = $('#student_addr').val();
        var short = $('#student_short').val();
        $.post(
            '/my_info/',
            {
                'id':id,
                'tel':tel,
                'email':email,
                'addr':addr,
                'short':short
            },
            function (data) {
                if (data['code']==='200'){
                    $('#student_tel').html(data['info'].student_tel);
                    $('#student_email').html(data['info'].student_email);
                    $('#student_addr').html(data['info'].student_addr);
                    $('#student_short').html(data['info'].student_short);
                    alert('信息修改成功')
                }else {
                    alert('信息错误')
                }
            }
        )
    })
})