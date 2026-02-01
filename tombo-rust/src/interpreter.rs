use crate::ast::{Expr, Stmt, Program, BinOp, UnOp};
use std::collections::HashMap;
use std::fmt;
use std::rc::Rc;
use std::cell::RefCell;

#[derive(Debug, Clone)]
pub enum Value {
    Integer(i64),
    Float(f64),
    String(String),
    Boolean(bool),
    List(Rc<RefCell<Vec<Value>>>),
    Dict(Rc<RefCell<HashMap<String, Value>>>),
    Function {
        params: Vec<String>,
        body: Vec<Stmt>,
        env: Rc<RefCell<Environment>>,
    },
    None,
}

impl Value {
    pub fn is_truthy(&self) -> bool {
        match self {
            Value::Boolean(b) => *b,
            Value::None => false,
            Value::Integer(n) => *n != 0,
            Value::Float(f) => *f != 0.0,
            Value::String(s) => !s.is_empty(),
            Value::List(l) => !l.borrow().is_empty(),
            Value::Dict(d) => !d.borrow().is_empty(),
            _ => true,
        }
    }

    pub fn to_string(&self) -> String {
        match self {
            Value::Integer(n) => n.to_string(),
            Value::Float(f) => f.to_string(),
            Value::String(s) => s.clone(),
            Value::Boolean(b) => b.to_string(),
            Value::None => "none".to_string(),
            Value::List(l) => {
                let items: Vec<String> = l.borrow().iter().map(|v| v.to_string()).collect();
                format!("[{}]", items.join(", "))
            }
            Value::Dict(d) => {
                let pairs: Vec<String> = d
                    .borrow()
                    .iter()
                    .map(|(k, v)| format!("\"{}\": {}", k, v.to_string()))
                    .collect();
                format!("{{{}}}", pairs.join(", "))
            }
            _ => "function".to_string(),
        }
    }
}

impl fmt::Display for Value {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

#[derive(Debug)]
pub struct Environment {
    vars: HashMap<String, Value>,
    parent: Option<Rc<RefCell<Environment>>>,
}

impl Environment {
    pub fn new() -> Self {
        Environment {
            vars: HashMap::new(),
            parent: None,
        }
    }

    pub fn with_parent(parent: Rc<RefCell<Environment>>) -> Self {
        Environment {
            vars: HashMap::new(),
            parent: Some(parent),
        }
    }

    pub fn set(&mut self, name: String, value: Value) {
        self.vars.insert(name, value);
    }

    pub fn get(&self, name: &str) -> Option<Value> {
        if let Some(value) = self.vars.get(name) {
            Some(value.clone())
        } else if let Some(parent) = &self.parent {
            parent.borrow().get(name)
        } else {
            None
        }
    }

    pub fn update(&mut self, name: &str, value: Value) -> Result<(), String> {
        if self.vars.contains_key(name) {
            self.vars.insert(name.to_string(), value);
            Ok(())
        } else if let Some(parent) = &self.parent {
            parent.borrow_mut().update(name, value)
        } else {
            Err(format!("Variable '{}' not found", name))
        }
    }
}

pub struct Interpreter {
    env: Rc<RefCell<Environment>>,
    return_value: Option<Value>,
    break_flag: bool,
    continue_flag: bool,
}

impl Interpreter {
    pub fn new() -> Self {
        let env = Rc::new(RefCell::new(Environment::new()));
        let mut interp = Interpreter {
            env,
            return_value: None,
            break_flag: false,
            continue_flag: false,
        };
        interp.setup_builtins();
        interp
    }

    fn setup_builtins(&mut self) {
        // Built-in functions will be handled in eval_call
    }

    pub fn evaluate(&mut self, program: &Program) -> Result<(), String> {
        for stmt in &program.statements {
            self.eval_stmt(stmt)?;
            if self.return_value.is_some() {
                break;
            }
        }
        Ok(())
    }

    fn eval_stmt(&mut self, stmt: &Stmt) -> Result<(), String> {
        if self.break_flag || self.continue_flag || self.return_value.is_some() {
            return Ok(());
        }

        match stmt {
            Stmt::Let { name, value } => {
                let val = self.eval_expr(value)?;
                self.env.borrow_mut().set(name.clone(), val);
                Ok(())
            }
            Stmt::Change { name, value } => {
                let val = self.eval_expr(value)?;
                self.env.borrow_mut().update(name, val)?;
                Ok(())
            }
            Stmt::Expr(expr) => {
                self.eval_expr(expr)?;
                Ok(())
            }
            Stmt::If {
                condition,
                then_body,
                elif_parts,
                else_body,
            } => {
                let cond_val = self.eval_expr(condition)?;
                if cond_val.is_truthy() {
                    for s in then_body {
                        self.eval_stmt(s)?;
                    }
                } else {
                    let mut executed = false;
                    for (elif_cond, elif_body) in elif_parts {
                        let elif_val = self.eval_expr(elif_cond)?;
                        if elif_val.is_truthy() {
                            for s in elif_body {
                                self.eval_stmt(s)?;
                            }
                            executed = true;
                            break;
                        }
                    }
                    if !executed {
                        if let Some(else_stmts) = else_body {
                            for s in else_stmts {
                                self.eval_stmt(s)?;
                            }
                        }
                    }
                }
                Ok(())
            }
            Stmt::While { condition, body } => {
                while self.eval_expr(condition)?.is_truthy() {
                    for s in body {
                        self.eval_stmt(s)?;
                        if self.break_flag {
                            self.break_flag = false;
                            return Ok(());
                        }
                        if self.continue_flag {
                            self.continue_flag = false;
                            break;
                        }
                        if self.return_value.is_some() {
                            return Ok(());
                        }
                    }
                }
                Ok(())
            }
            Stmt::For { var, iter, body } => {
                let iter_val = self.eval_expr(iter)?;
                let items = match iter_val {
                    Value::List(l) => l.borrow().clone(),
                    Value::String(s) => s.chars().map(|c| Value::String(c.to_string())).collect(),
                    _ => return Err("Cannot iterate over non-iterable".to_string()),
                };

                for item in items {
                    self.env.borrow_mut().set(var.clone(), item);
                    for s in body {
                        self.eval_stmt(s)?;
                        if self.break_flag {
                            self.break_flag = false;
                            return Ok(());
                        }
                        if self.continue_flag {
                            self.continue_flag = false;
                            break;
                        }
                        if self.return_value.is_some() {
                            return Ok(());
                        }
                    }
                }
                Ok(())
            }
            Stmt::FnDef { name, params, body } => {
                let func = Value::Function {
                    params: params.clone(),
                    body: body.clone(),
                    env: Rc::clone(&self.env),
                };
                self.env.borrow_mut().set(name.clone(), func);
                Ok(())
            }
            Stmt::Return(expr) => {
                let val = if let Some(e) = expr {
                    self.eval_expr(e)?
                } else {
                    Value::None
                };
                self.return_value = Some(val);
                Ok(())
            }
            Stmt::Break => {
                self.break_flag = true;
                Ok(())
            }
            Stmt::Continue => {
                self.continue_flag = true;
                Ok(())
            }
            Stmt::Pass => Ok(()),
        }
    }

    fn eval_expr(&mut self, expr: &Expr) -> Result<Value, String> {
        match expr {
            Expr::Integer(n) => Ok(Value::Integer(*n)),
            Expr::Float(f) => Ok(Value::Float(*f)),
            Expr::String(s) => Ok(Value::String(s.clone())),
            Expr::Boolean(b) => Ok(Value::Boolean(*b)),
            Expr::Identifier(name) => {
                self.env
                    .borrow()
                    .get(name)
                    .ok_or_else(|| format!("Undefined variable: {}", name))
            }
            Expr::BinaryOp { left, op, right } => {
                let left_val = self.eval_expr(left)?;
                let right_val = self.eval_expr(right)?;
                self.eval_binop(&left_val, *op, &right_val)
            }
            Expr::UnaryOp { op, expr } => {
                let val = self.eval_expr(expr)?;
                self.eval_unop(*op, &val)
            }
            Expr::Call { func, args } => {
                let func_val = self.eval_expr(func)?;
                let arg_vals: Result<Vec<_>, _> = args.iter().map(|a| self.eval_expr(a)).collect();
                self.eval_call(&func_val, arg_vals?)
            }
            Expr::List(elements) => {
                let vals: Result<Vec<_>, _> = elements.iter().map(|e| self.eval_expr(e)).collect();
                Ok(Value::List(Rc::new(RefCell::new(vals?))))
            }
            Expr::Dict(pairs) => {
                let mut map = HashMap::new();
                for (k, v) in pairs {
                    let key = self.eval_expr(k)?.to_string();
                    let value = self.eval_expr(v)?;
                    map.insert(key, value);
                }
                Ok(Value::Dict(Rc::new(RefCell::new(map))))
            }
            Expr::Index { object, index } => {
                let obj_val = self.eval_expr(object)?;
                let idx_val = self.eval_expr(index)?;
                match obj_val {
                    Value::List(l) => {
                        if let Value::Integer(i) = idx_val {
                            let list = l.borrow();
                            let idx = if i < 0 {
                                (list.len() as i64 + i) as usize
                            } else {
                                i as usize
                            };
                            Ok(list
                                .get(idx)
                                .cloned()
                                .ok_or_else(|| "Index out of bounds".to_string())?)
                        } else {
                            Err("List index must be integer".to_string())
                        }
                    }
                    Value::Dict(d) => {
                        let key = idx_val.to_string();
                        Ok(d.borrow()
                            .get(&key)
                            .cloned()
                            .ok_or_else(|| format!("Key '{}' not found", key))?)
                    }
                    Value::String(s) => {
                        if let Value::Integer(i) = idx_val {
                            let idx = if i < 0 {
                                (s.len() as i64 + i) as usize
                            } else {
                                i as usize
                            };
                            Ok(Value::String(
                                s.chars()
                                    .nth(idx)
                                    .ok_or_else(|| "Index out of bounds".to_string())?
                                    .to_string(),
                            ))
                        } else {
                            Err("String index must be integer".to_string())
                        }
                    }
                    _ => Err("Cannot index non-indexable value".to_string()),
                }
            }
            _ => Err("Unimplemented expression".to_string()),
        }
    }

       fn eval_binop(&self, left: &Value, op: BinOp, right: &Value) -> Result<Value, String> {
        match (left, right) {
            (Value::Integer(a), Value::Integer(b)) => {
                match op {
                    BinOp::Add => Ok(Value::Integer(a + b)),
                    BinOp::Subtract => Ok(Value::Integer(a - b)),
                    BinOp::Multiply => Ok(Value::Integer(a * b)),
                    BinOp::Divide => {
                        if *b == 0 {
                            Err("Division by zero".to_string())
                        } else {
                            Ok(Value::Float(*a as f64 / *b as f64))
                        }
                    }
                    BinOp::FloorDivide => {
                        if *b == 0 {
                            Err("Division by zero".to_string())
                        } else {
                            Ok(Value::Integer(a / b))
                        }
                    }
                    BinOp::Modulo => {
                        if *b == 0 {
                            Err("Division by zero".to_string())
                        } else {
                            Ok(Value::Integer(a % b))
                        }
                    }
                    BinOp::Power => Ok(Value::Integer(a.pow(*b as u32))),
                    BinOp::Equal => Ok(Value::Boolean(a == b)),
                    BinOp::NotEqual => Ok(Value::Boolean(a != b)),
                    BinOp::Less => Ok(Value::Boolean(a < b)),
                    BinOp::Greater => Ok(Value::Boolean(a > b)),
                    BinOp::LessEqual => Ok(Value::Boolean(a <= b)),
                    BinOp::GreaterEqual => Ok(Value::Boolean(a >= b)),
                    BinOp::BitwiseAnd => Ok(Value::Integer(a & b)),
                    BinOp::BitwiseOr => Ok(Value::Integer(a | b)),
                    BinOp::BitwiseXor => Ok(Value::Integer(a ^ b)),
                    BinOp::LeftShift => Ok(Value::Integer(a << b)),
                    BinOp::RightShift => Ok(Value::Integer(a >> b)),
                    BinOp::And => Err("Logic operators not compatible with integers".to_string()),
                    BinOp::Or => Err("Logic operators not compatible with integers".to_string()),
                }
            }
            (Value::Float(_), _) | (_, Value::Float(_)) => {
                let a_f = match left {
                    Value::Float(f) => *f,
                    Value::Integer(i) => *i as f64,
                    _ => return Err("Type mismatch for operation".to_string()),
                };
                let b_f = match right {
                    Value::Float(f) => *f,
                    Value::Integer(i) => *i as f64,
                    _ => return Err("Type mismatch for operation".to_string()),
                };
                match op {
                    BinOp::Add => Ok(Value::Float(a_f + b_f)),
                    BinOp::Subtract => Ok(Value::Float(a_f - b_f)),
                    BinOp::Multiply => Ok(Value::Float(a_f * b_f)),
                    BinOp::Divide => {
                        if b_f == 0.0 {
                            Err("Division by zero".to_string())
                        } else {
                            Ok(Value::Float(a_f / b_f))
                        }
                    }
                    BinOp::FloorDivide => {
                        if b_f == 0.0 {
                            Err("Division by zero".to_string())
                        } else {
                            Ok(Value::Float((a_f / b_f).floor()))
                        }
                    }
                    BinOp::Modulo => Ok(Value::Float(a_f % b_f)),
                    BinOp::Power => Ok(Value::Float(a_f.powf(b_f))),
                    BinOp::Equal => Ok(Value::Boolean((a_f - b_f).abs() < 1e-10)),
                    BinOp::NotEqual => Ok(Value::Boolean((a_f - b_f).abs() >= 1e-10)),
                    BinOp::Less => Ok(Value::Boolean(a_f < b_f)),
                    BinOp::Greater => Ok(Value::Boolean(a_f > b_f)),
                    BinOp::LessEqual => Ok(Value::Boolean(a_f <= b_f)),
                    BinOp::GreaterEqual => Ok(Value::Boolean(a_f >= b_f)),
                    BinOp::BitwiseAnd | BinOp::BitwiseOr | BinOp::BitwiseXor | BinOp::LeftShift | BinOp::RightShift => {
                        Err("Bitwise operations only work on integers".to_string())
                    }
                    _ => Err("Invalid operation for floats".to_string()),
                }
            }
            (Value::String(a), Value::String(b)) => {
                match op {
                    BinOp::Add => Ok(Value::String(format!("{}{}", a, b))),
                    BinOp::Equal => Ok(Value::Boolean(a == b)),
                    BinOp::NotEqual => Ok(Value::Boolean(a != b)),
                    _ => Err("Invalid string operation".to_string()),
                }
            }
            (Value::Boolean(a), Value::Boolean(b)) => {
                match op {
                    BinOp::And => Ok(Value::Boolean(*a && *b)),
                    BinOp::Or => Ok(Value::Boolean(*a || *b)),
                    BinOp::Equal => Ok(Value::Boolean(a == b)),
                    BinOp::NotEqual => Ok(Value::Boolean(a != b)),
                    _ => Err("Invalid boolean operation".to_string()),
                }
            }
            _ => Err("Type mismatch for operation".to_string()),
        }
    }

    fn eval_unop(&self, op: UnOp, val: &Value) -> Result<Value, String> {
        match op {
            UnOp::Negate => match val {
                Value::Integer(n) => Ok(Value::Integer(-n)),
                Value::Float(f) => Ok(Value::Float(-f)),
                _ => Err("Cannot negate non-numeric value".to_string()),
            },
            UnOp::Not => Ok(Value::Boolean(!val.is_truthy())),
            UnOp::BitwiseNot => match val {
                Value::Integer(n) => Ok(Value::Integer(!n)),
                _ => Err("Bitwise not only works on integers".to_string()),
            },
        }
    }

    fn eval_call(&mut self, func: &Value, args: Vec<Value>) -> Result<Value, String> {
        match func {
            Value::Function { params, body, env } => {
                if params.len() != args.len() {
                    return Err(format!(
                        "Function expects {} arguments, got {}",
                        params.len(),
                        args.len()
                    ));
                }

                let fn_env = Rc::new(RefCell::new(Environment::with_parent(Rc::clone(env))));
                for (param, arg) in params.iter().zip(args.iter()) {
                    fn_env.borrow_mut().set(param.clone(), arg.clone());
                }

                let prev_env = Rc::clone(&self.env);
                self.env = fn_env;

                for stmt in body {
                    self.eval_stmt(stmt)?;
                    if let Some(val) = self.return_value.take() {
                        self.env = prev_env;
                        return Ok(val);
                    }
                }

                self.env = prev_env;
                Ok(Value::None)
            }
            _ => {
                // Check for built-in functions by name
                // Need to handle this differently since func is not a String
                Err("Cannot call non-function".to_string())
            }
        }
    }
}

impl Default for Interpreter {
    fn default() -> Self {
        Self::new()
    }
}
