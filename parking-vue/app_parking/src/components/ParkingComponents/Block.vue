<template>
    <button class="button">
        <div>
            {{block.startTime}} - {{block.endTime}}
        </div>
    </button>
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
        // getPlage(){
        //     foreach (plage in plagesBlock);{
        //         if (plage.startTime == block.startTime && plage.endTime == block.endTime){
        //             plage = plageBlock;
        //         }
        //     }
        // },
    },
    created() {
        //this.getPlage();
        console.log(this.plagesBlock);
    }    
}
</script>
