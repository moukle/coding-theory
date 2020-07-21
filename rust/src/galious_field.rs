// use ndarray::arr2;
// use rand;
use std::fmt;
use primes::is_prime;
use polynomial::Polynomial;

struct GaliousField {
    p: u32,
    d: u32,
    q: u32
}

fn permurtation(l1: Vec<u32>, l2: Vec<u32>) -> bool {
    // dirty non linear solution
    // TODO: use counters
    return l1.sort() == l2.sort()
}

impl fmt::Display for GaliousField {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        let str = format!("GF(p={}, d={}, q={})", self.p, self.d, self.q);
        fmt.write_str(&str)?;
        Ok(())
    }
}

impl GaliousField {
    fn new(p: u32, d: u32) -> GaliousField {
        if is_prime(p.into()) {
            GaliousField {
                p: p,
                d: d,
                q: p.pow(d)
            }
        }
        else {
            println!("p ({}) is not prime, abording", p);
            GaliousField {p:0, d:0, q:0}
        }
    }

    fn primitve(&self) -> u32 {
        let gf_star = (1..self.q).collect::<Vec<u32>>();

        let mut ei;
        for e in &gf_star {
            ei = c![self.r#mod(e.pow(i)), for i in 0..self.q-1];
            // println!("{:?}", ei);
            if permurtation(ei, gf_star) {
                return *e;
            }
        }
        0
    }

    fn r#mod(&self, x: u32) -> u32 {
        // currently only for d=1
        x % self.q
    }
}

pub fn run() {
    let gf = GaliousField::new(7, 1);
    println!("{}", gf);
    println!("{}", gf.primitve());

    let p = Polynomial::new(vec![1,1]);
    let p2 = Polynomial::new(vec![1,1]);
    let pp = &p * &p2;
    println!("p = {}", p.pretty("x"));
    println!("p^2 = {}", pp.pretty("x"));
}
