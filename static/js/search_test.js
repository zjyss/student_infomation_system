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
                '/search_test/',
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
