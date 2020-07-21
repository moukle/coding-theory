use std::fmt;

struct Polynomial {
    coefficients: Vec<u8>
}

impl fmt::Display for Polynomial {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        let mut str_add: String = "".to_string();
        let mut str_x:   String = "".to_string();
        let mut int_pow = 0;
        for c in &self.coefficients {
            fmt.write_str(&str_add)?;
            fmt.write_str(&c.to_string())?;
            fmt.write_str(&str_x)?;
            int_pow += 1;
            str_add  = " + ".to_string();
            str_x    = format!("x^{}", int_pow);
        }
        Ok(())
    }
}

impl Polynomial {
    fn new(coeffs: Vec<u8>) -> Polynomial {
        Polynomial {
            coefficients: coeffs
        }
    }
}

pub fn run() {
    let p = Polynomial::new(vec![1,2,3]);
    println!("Polynomial: {}", p)
}
