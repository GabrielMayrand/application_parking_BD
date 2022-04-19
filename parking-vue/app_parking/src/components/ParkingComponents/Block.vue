<template>
    <div>
        <button class="button">
            <div>
            {{block.startTime}}
        </div>
        <div>
            -
        </div>
        <div>
            {{block.endTime}}
        </div>
        </button>
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
