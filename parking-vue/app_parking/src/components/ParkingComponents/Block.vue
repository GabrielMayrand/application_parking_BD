<template>
    <div class="card">
        <div>
            {{block.startTime}}
        </div>
        <div>
            {{block.endTime}}
        </div>
    </div>
</template>

<script>


export default {
    data() {
        return {
            plageBlock: Object,
        }
    },
    props:{
        block: Object,
        plagesBlock: Array,
    },
    methods :{
        getPlage(){
            this.plagesBlock.every(plage => {
                if(plage.startTime == this.block.startTime){
                    this.plageBlock = plage;
                    return false;
                }
            });
        },
    }
}
</script>
