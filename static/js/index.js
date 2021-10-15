let vm = new Vue({
    el: '#content',
    data: {
        infolist: '',
    },
    methods: {
        getinfo: function () {
            var id = sessionStorage.getItem('id');
            $.post(
                '/log_in/',
                {
                    'id': id
                },
                function (data) {
                    if (data['code']==='400'){
                        window.location.href='/'
                    }else {
                        vm.infolist = data;
                        console.log(vm.infolist)
                    }
                }
            )
        }
    },
    mounted() {
        this.getinfo();
    }
});
