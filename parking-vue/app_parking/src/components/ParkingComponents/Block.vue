<template>
    <div class="card">
        <div>
            {{this.block.startTime}}
        </div>
        <div>
            {{this.block.endTime}}
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
