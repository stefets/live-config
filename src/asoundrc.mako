pcm.SD90 {
 	type dmix
 	ipc_key 100
 	slave {
		pcm "${SD90}"
	}
	bindings {
		0 0
		1 1
	}
}

pcm.U192k {
 	type dmix
 	ipc_key 300
 	slave {
		pcm "${U192k}"
	}
	bindings {
		0 0
		1 1
	}
}
