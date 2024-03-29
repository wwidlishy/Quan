# Quan
 A general purpuse functional compiled language

# Languages Premise

Quan is designed to be a simple functional language.  
That teaches people the basics of the functional programming paradigm.  
And is also general purpuse, however was put in mind for linux/windows CLI/GUI programs.  
It is ment to be the Python of Functional Languages.

q stands for: Quick  
u stands for: understandable  
a stands for: to assembly  
n stands for: novice friendly  

# Quan Preview

Be **Bold**!  
Each statement ends with a semicollon!

```c
print("Quan is beuatiful"); // this is an example statement, it must be in a function
```

There are two types of variable declarations.  
Mutable variable declaration:
```c
// This is a mutable variable, it's value can change
mute a: Integer = 10;

// Mutation is unsafe, to prevent unwanted changes for a functions local mutable,
// you can specify the number of times it can mutate

fn entry()
{
    mute(2) result: Integer = 4; // this mutable can mutate only 2 times per function cycle
    result++;                             // this is just result += 1   [First mutation]
    result *= 2;                         // [Second mutation]
    // result += result / 2         // [Third mutation], Would be an error!
};
```
Or Imutable variables, which no matter how much you please & beg won't mutate:
```c
fn five()
{
    imute result: Integer = 5;
};

fn entry()
{
    // The variable checker prioritizes local variables
    // Since five didn't exits in this scope before, it would pick the global one (our function)
    imute five: Integer = @global five();
    imute result: Integer = 0;
    print(five -> String);      // print supports only strings
};
```

**Note:** the variable `result` decides of output and return type of the function.  

Loops are a relic of the past!  
In Quan there are no loops!  
We use recursion instead.  

**Note:** You can recurse forever  
**Another Note:** Organize functions with `namespaces`  
**Yet Another Note:** Mutables and Imutables of a functions are fred after each function cycle

```c
// For redability purpuses make sure to name your namespaces after functions they "belong" to,
// so for entry it will be _entry

namespace _entry
{
    fn truthMachine(imute input: Integer(0, 1))
    {
        // custom type: Integer with possible values of 0 and 1
        imute result: Integer(0, 1) = input; // do `imute result: Integer(1-10) = 1` for a type ranged 1 to 10 including both sides
        // or`imute result: Integer(1-10, 15-20) = 1` for a type ranged 1 to 10 and 15-20 including both sides
        // @self = this function
        // if you do `truthMachine(result)` it will return an error bcz it is not defined yet
        if result: @self (result); // if result == 1 calls itself with result, forever recursion. 
        //multiline if would be if (condition) {...}// 
    };

    fn handleInput()
    {
        imute result: String(1) = getStringInput("0 / 1 >>> "); // String cut to be 1 char long
        if ! ["0", "1"].has(result): handleInput(); // Recurse until a valid input
    };
};

fn entry()
{
    imute result: Integer = 0;
    imute input: Integer(0, 1) = _entry.handleInput() -> Integer(0, 1);
    _entry.truthMachine(input);
};
```

Okay, listen to me.  
When it comes to if statements there are 2 syntaxes you can mix: one and multiline if  
The keywords are: `if`, `elsif`, `else`.  

```c
fn entry()
{
    mute(1) result: Integer(0-2) = -1;
    if 2 + 2 == 5: result = 1;
    elsif (16.root(2) == 4) {
        result = 0;
    }
    else: result = 2;
};
```

As in many other languages, arrays are encapsolated in `[]`.  
Here is a simple list usage

```c
fn sum_arr(imute a: Array, imute current_sum: Number = 0, imute index: Integer = 0)
{
    mute(1) result: Number = current_sum;
    imute nextIndex: Integer = index + 1;

    if index.isValidIndexOf(a): result = @self (a, current_sum + a[index], nextIndex);
    else: result = current_sum;
};

fn entry()
{
    imute result: Integer = sum_arr([-3, 3]); // An array can hold multiple types
};```

Also there are lambdas.  

```c
imute inc: Fn = lambda(imute x: Integer): Integer x + 1;

fn entry()
{
    mute(2) result: Integer = -2;
    result = inc(result);           // Increment using inc function
    result = result.inc();          // In Quan x.f(...) = f(x, ...)
    // (a, b, c).f(...) = f(a, b, c, ...)
};
```

In python there is a **kwargs system,  
N of an argument.  
In Quan it is used like this:  

```c
// `args` as an argument is reserved for kwargs, must be Array type
// You can have only one `args`, and arguments can be before and after `args`

fn sum(imute args: Array, imute sum: Number = 0)
{
    mute(1) result: Number = sum;
    imute nextIndex: Integer = 1;

    // Note: # in `#args[1:args.lastIndex()]` means to extract the list,
    // so: f([a, b]) = f([a, b]); f(#[a, b]) = f(a, b)

    if nextIndex.isValidIndexOf(args): result += args[0] + @self (#args[1:args.lastIndex()]);
    else: result += args[0];
};

fn entry()
{
    imute result: Integer = sum(-3, 3, -4, 4);
    print(result -> String);
};
```