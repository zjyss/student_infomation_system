let vm = new Vue({
    el: '#content',
    data: {
        infolist: '',
        lesson_list : '',
        teacher_list : ''
    },
    methods: {
        getinfo: function () {
            var id = sessionStorage.getItem('id');
            $.post(
                '/get_test/',
                {
                    'id': id
                },
                function (data) {
                    vm.infolist = data[0];
                    vm.lesson_list = data[1];
                    // vm.teacher_list = data[2];
                    console.log(data)
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
        var lesson_name = $('input:radio:checked').val();
        alert(lesson_name)
        $.post(
            '/get_test/',
            {
                'id':id,
                'lesson_name':lesson_name
            },
            function (data) {
                $('#message').html(data);
                console.log(data)
            }
        )
    })
})