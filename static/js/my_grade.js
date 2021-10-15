let vm = new Vue({
    el: '#content',
    data: {
        infolist: '',
        lesson_list : '',
        grade_list : []
    },
    methods: {
        getinfo: function () {
            var id = sessionStorage.getItem('id');
            $.post(
                '/my_grades/',
                {
                    'id': id
                },
                function (data) {
                    vm.infolist = data[0];
                    vm.lesson_list = data[1];
                    for (var i =0;i<6;i++){
                        vm.grade_list.push(data[2][i]['grade'])
                    }
                    console.log(data);
                    console.log(vm.grade_list)
                }
            )
        }
    },
    mounted() {
        this.getinfo();
    }
});
