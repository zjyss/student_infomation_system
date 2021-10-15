let vm = new Vue({
    el: '#content',
    data: {
        examlist: [],
        exam_getlist : [],
        infolist : []
    },
    methods: {
        //这个ajax用来请求header的用户姓名和学号
        getname: function () {
            var id = sessionStorage.getItem('id');
            $.post(
                '/get_exam/',
                {
                    'id':id
                },
                function (data) {
                    vm.examlist = data['examlist'];
                    vm.exam_getlist = data['exam_get_list'];
                    vm.infolist = data['student'];
                    console.log(vm.examlist);
                    console.log(vm.exam_getlist)
                }
            )
        }
    },
    mounted(){
        this.getname();
    },

});
//添加考试
$(function () {
    $('#btn_add').click(function (event) {
        event.preventDefault();
        var id = sessionStorage.getItem('id');
        var exam_name = $("input[type='radio']:checked").val();
        $.post(
            '/get_exam/',
            {
                'id':id,
                'exam_name':exam_name
            },
            function (data) {
                if (data['code']==='200'){
                    alert('添加成功');
                    window.location.reload()
                }else {
                    alert('添加失败')
                }
            }
        )
    })
})
$(function () {
    $('#btn_del').click(function (event) {
        event.preventDefault();
        var id = sessionStorage.getItem('id');
        var exam_name = $("input[type='radio']:checked").val();
        $.post(
            '/exam_check/',
            {
                'id':id,
                'exam_name':exam_name
            },
            function (data) {
                if (data['code']==='200'){
                    alert('删除成功');
                    $("input[type='radio']:checked").parent().parent().remove()
                }else {
                    alert('删除失败')
                }
            }
        )
    })
})