<script>
import axios from 'axios';

export default {
    data() {
        return {
            tasks: []
        };
    },
    methods: {
        fetchTasks() {
          alert("dasd");
            axios.get('http://localhost:8000/scheduler/api/tasks/')
                .then(response => {
                    this.tasks = response.data;
                })
                .catch(error => {
                    console.error('Error fetching tasks:', error);
                });
        }
    },
    mounted() {
        this.fetchTasks();
    }
};
</script>