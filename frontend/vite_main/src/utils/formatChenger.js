// I created this function because I need to do things that the BACKEND needs to do 
// but he strongarmed me into doing such work as he is too busy with the act of 
// goofing around instead of doing the minimum effort to solve this trivial python problem that
// has plagued this code for eons.
export function aaaaa(dictionary, name) {
    if (dictionary.hasOwnProperty(name)) {
      return dictionary[name];
    }
    for (let key in dictionary) {
      if (dictionary[key] === name) {
        return key; 
      }
    }
    return null; 
  }
  


export function getRandomDiseases(diseases) {
        
    const sortedDiseases = Object.entries(diseases).sort((a, b) => b[1] - a[1]);
    

    const topDiseases = sortedDiseases.slice(0, 6);
    const toReturn = []
    const bottomDiseases = sortedDiseases.slice(-20);
    const selectedTopDiseasesCount = Math.floor(Math.random() * 2) + 1;  
    const selectedTopDiseases = topDiseases.slice(0, selectedTopDiseasesCount);
    for (let i in selectedTopDiseases)
    {
        toReturn.push(selectedTopDiseases[i][0])
    }
    
    const bottom = sortedDiseases.slice(-20, -1);

    for (let i = 6 - toReturn.length; i > 0; i--)
    {
        let aux = bottom[Math.floor(Math.random()*19)][0];
        if (!toReturn.includes(aux))
        {
            toReturn.push(aux);
        }
        else{
            i++;
        }
    }
    return toReturn;
    }
    