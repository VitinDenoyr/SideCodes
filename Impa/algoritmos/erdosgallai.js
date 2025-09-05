function getGraphData(d){ //d = lista de números se aprovada por validate(d) e por evenSum(d). Essa função retorna as arestas de um grafo simples
    // Variáveis
    let n = d.length; // Quantidade de inteiros
    d.sort((a,b) => b-a); // Garante ordem decrescente
    let v = Array(n).fill(0); // Subrealização atual
    let r = 0; // Índice crítico como no algoritmo
    let adj = Array(n); // Matriz de adjacência do grafo
    for(let i = 0; i < n; i++) adj[i] = Array(n).fill(false);

    // Métodos auxiliares
	function hasFreeConnection(){
		let listOfFrees = [];
		for(let i = 0; i < n; i++){
            if(i == r) continue;
			if(d[i] > v[i] && adj[i][r] === false) listOfFrees.push(i);
		}
		if(listOfFrees.length > 0){
            const rand = (Math.floor(Math.random() * 997))%(listOfFrees.length);
            return listOfFrees[rand];
        }
		return n+1;
	}

	function findMinimalDisconnected(){
		for(let i = 0; i < n; i++){
            if(i == r) continue;
			if(adj[i][r] === false) return i;
		}
		return n+1;
	}

	function findTrickyVertexAboveR(){
		for(let i = r+1; i < n; i++){
			if(v[i] < Math.min(r+1,d[i])) return i;
		}
		return n+1;
	}

	function getPairBelowR(){
		for(let i = 0; i < r; i++){
			for(let j = i+1; j < r; j++){
				if(adj[i][j] == false) return [i,j];
			}
		}
		return [n+1,n+1];
	}

    function findU(vi){ 
        for(let i = 0; i < n; i++){
            if(i == r || i == vi || adj[i][vi] == 0 || adj[i][r] == 1) continue;
            return i;
        }
    }

    function findK(){
        for(let i = r+1; i < n; i++){
            if(d[i] > v[i]) return i;
        }
    }

    function findIandU(vk){ 
        let vi = n+1;
        for(let i = 0; i < r; i++){
            if(adj[vk][i] == 0){
                vi = i; break;
            }
        }
        for(let i = 0; i < n; i++){
            if(i == r || i == vi || i == vk || adj[i][vi] == 0 || adj[i][r] == 1) continue;
            return [vi, i];
        }
    }

    function findUandW(vi,vj){
        let u = -1, w = -1;
        for(let k = r+1; k < n; k++){
            if(adj[k][r] === true) continue;
            if((u === -1) && (adj[k][vi] === true)){
                u = k;
            }
            if((w === -1) && (adj[k][vj] === true)){
                w = k;
            }
            if((u !== -1) && (w !== -1)) return [u,w];
        }
        return [u,w];
    }

    // Execução do algoritmo
    while(r < n){
        if(d[r] == v[r]){
            r++; continue;
        }
        let state = hasFreeConnection();
        // Caso 0
        if(state < n){ 
            let vi = state;
            adj[vi][r] = true; adj[r][vi] = true;
            v[vi]++; v[r]++;
        }
        // Caso 1
        else if((state = findMinimalDisconnected()) < r){ 
            let vi = state;
            let u = findU(vi);
            if(d[r] - v[r] == 1){
                let vk = findK();
                adj[r][vk] = false; adj[vk][r] = false;
                v[r]--; v[vk]--;
            }
            adj[u][vi] = false; adj[vi][u] = false;
            adj[u][r] = true; adj[r][u] = true;
            adj[vi][r] = true; adj[r][vi] = true;
            v[r] += 2;
        } 
        // Caso 2
        else if((state = findTrickyVertexAboveR()) < n){ 
            let vk = state, vi, u;
            [vi,u] = findIandU(vk);
            adj[u][vi] = false; adj[vi][u] = false;
            adj[u][r] = true; adj[r][u] = true;
            adj[vi][vk] = true; adj[vk][vi] = true;
            v[r]++; v[vk]++;
        } 
        // Caso 3
        else if((state = getPairBelowR()).toString() !== [n+1,n+1].toString()){
            let vi = state[0], vj = state[1], u, w;
            [u,w] = findUandW(vi,vj);
            adj[u][vi] = false; adj[vi][u] = false;
            adj[w][vj] = false; adj[vj][w] = false;
            adj[vi][vj] = true; adj[vj][vi] = true;
            adj[u][r] = true; adj[r][u] = true;
            v[r]++; v[w]--;
        } 
        else {
            r++; continue;
        }
    }

    res = [];
    res.push(d);
    for(let i = 1; i < n; i++){
        for(let j = 0; j < i; j++){
            if(adj[i][j] == 1){
                res.push([j,i]);
            }
        }
    }
    return res;
}