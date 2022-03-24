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
            plage: Object,
        }
    },
    props:{
        block: Object,
        plagesBlock: Array,
    },
    methods :{
        //get plage of this block
        getPlage(){
            this.plagesBlock.every(plage => {
                if(plage.startTime == this.block.startTime){
                    this.plage = plage;
                    return false;
                }
            });
        },
    }
}
</script>
