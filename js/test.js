var obj = {
    name: "Carrot",
    "for": "Max",//'for' 是保留字之一，使用'_for'代替
    details: {
        color: "orange",
        size: 12
    }
}
console.log(obj.for)
obj.for = "Simon2";
console.log(obj.for)

var a = ["dog", "cat", "hen"];
a[100] = "fox";
a.length; // 101

console.log(typeof(obj))
