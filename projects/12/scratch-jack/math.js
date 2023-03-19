const twoToThe = new Array(16);

function initArray(){
    let i = 1;
    twoToThe[0] = 1;

    while(i < 16){
        twoToThe[i] = i + i;
    }

    twoToThe[15] = -32767;
}

function bit(x, y){
        let trueBits = new Array(16);
        let i = 0;
        let sumOf = 0;

        while(i < 16){
            if (twoToThe[i] > x){
                let ii = i - 1;
                while(ii > 0){
                    if((twoToThe[ii] + sumOf) > x){
                        trueBits[ii] = false;
                        ii = i - 1;
                    }
                    sumOf = sumOf + twoToThe[ii];
                    trueBits[ii] = true;
                    ii = i - 1;
                }
            }
            i = i + 1;
            trueBits[i] = false;
        }

        return trueBits[j];
}

initArray()
console.log(bit(500,9));