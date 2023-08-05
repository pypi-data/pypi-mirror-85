use rand::distributions::Uniform;
use rand::{thread_rng, Rng};

use rayon::prelude::*;

pub mod eq;
pub mod le;
pub mod stream;
pub mod utils;

// Byte precision and security.
pub const N: usize = 4;
pub const L: usize = 16;

fn build_params(op_id: usize) -> (usize, usize, usize) {
    let (keylen, n_aes_keys) = match op_id {
        1 => (1205, 4),
        // 1 => (1304, 4),
        _ => (597, 2),
    };

    // TODO: small inputs
    let n_aes_streams = 128;

    (n_aes_keys, keylen, n_aes_streams)
}

#[no_mangle]
pub unsafe extern "C" fn keygen(
    keys_a_pointer: *mut u8,
    keys_b_pointer: *mut u8,
    n_values: usize,
    n_threads: usize,
    op_id: usize,
) {
    assert!(!keys_a_pointer.is_null());
    assert!(!keys_b_pointer.is_null());

    let (n_aes_keys, keylen, n_aes_streams) = build_params(op_id);

    // Generate AES-128 keys for MMO (expansion factor 2 or 4)
    let mut rng = rand::thread_rng();
    let mut aes_keys = Vec::new();
    // let aes_keys: [u128; n_aes_keys] = rng.gen();
    // let aes_keys: Vec<u128> = rng.sample_iter(Uniform).take(n_aes_keys).collect();

    // Write the AES key to the first line of the key block.
    // The rest of the line is empty (we keep a Numpy array shape).
    for i in 0..n_aes_keys {
        let aes_key = rng.gen();
        aes_keys.push(aes_key);
        utils::write_aes_key_to_raw_line(aes_key, keys_a_pointer.add(L * i) as *mut u8);
        utils::write_aes_key_to_raw_line(aes_key, keys_b_pointer.add(L * i) as *mut u8);
    }

    let mut key_stream_args = vec![];
    let mut line_counter = 1; // The first line is taken by the AES key.
    let default_length = n_values / n_aes_streams;
    let n_longer_streams = n_values % n_aes_streams;
    let mut stream_length: usize;

    for stream_id in 0..n_aes_streams {
        // The first streams work a bit more if necessary
        if stream_id < n_longer_streams {
            stream_length = default_length + 1;
        } else {
            stream_length = default_length;
        }

        if stream_length > 0 {
            // Cast raw pointers to a type that can be sent to threads
            key_stream_args.push((
                stream_id,
                stream_length,
                keys_a_pointer.add(keylen * line_counter) as usize,
                keys_b_pointer.add(keylen * line_counter) as usize,
            ));
            line_counter += stream_length;
        }
    }

    // Each thread will repeatedly execute this closure in parallel
    let create_keypair = |key_stream_arg: &(usize, usize, usize, usize)| -> () {
        let (stream_id, stream_length, key_a_pointer, keys_b_pointer) = *key_stream_arg;
        stream::generate_key_stream(
            &aes_keys,
            stream_id,
            stream_length,
            key_a_pointer,
            keys_b_pointer,
            op_id,
        );
    };

    // Force Rayon to use the number of thread provided by the user, unless a pool already exists
    rayon::ThreadPoolBuilder::new()
        .num_threads(n_threads)
        .build_global();
    key_stream_args.par_iter().for_each(create_keypair);
}

#[no_mangle]
pub unsafe extern "C" fn eval(
    party_id: usize,
    xs_pointer: *const u8,
    keys_pointer: *const u8,
    results_pointer: *mut i64,
    n_values: usize,
    n_threads: usize,
    op_id: usize,
) {
    assert!(!xs_pointer.is_null());
    assert!(!keys_pointer.is_null());
    assert!(!results_pointer.is_null());

    let (n_aes_keys, keylen, n_aes_streams) = build_params(op_id);

    // Read the AES keys from the first line of the key block.
    let mut aes_keys = Vec::new();
    for i in 0..n_aes_keys {
        aes_keys.push(utils::read_aes_key_from_raw_line(
            keys_pointer.add(L * i) as *mut u8
        ));
    }

    let mut key_stream_args = vec![];
    let mut line_counter = 0;
    let default_length = n_values / n_aes_streams;
    let n_longer_streams = n_values % n_aes_streams;
    let mut stream_length: usize;

    for stream_id in 0..n_aes_streams {
        // The first streams work a bit more if necessary
        if stream_id < n_longer_streams {
            stream_length = default_length + 1;
        } else {
            stream_length = default_length;
        }

        if stream_length > 0 {
            // Cast raw pointers to a type that can be sent to threads
            key_stream_args.push((
                stream_id,
                stream_length,
                xs_pointer.add(N * line_counter) as usize,
                keys_pointer.add(keylen * (line_counter + 1)) as usize,
                results_pointer.add(line_counter) as usize,
            ));
            // The first line is taken by the AES key.
            line_counter += stream_length;
        }
    }

    // Each thread will repeatedly execute this closure in parallel
    let eval_key = |key_stream_arg: &(usize, usize, usize, usize, usize)| -> () {
        let (stream_id, stream_length, x_pointer, key_pointer, result_pointer) = *key_stream_arg;
        stream::eval_key_stream(
            party_id as u8,
            &aes_keys,
            stream_id,
            stream_length,
            x_pointer,
            key_pointer,
            result_pointer,
            op_id,
        );
    };

    // Force Rayon to use the number of thread provided by the user, unless a pool already exists
    rayon::ThreadPoolBuilder::new()
        .num_threads(n_threads)
        .build_global();
    key_stream_args.par_iter().for_each(eval_key);
}
