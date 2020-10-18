from proxmoxer import ProxmoxAPI
proxmox = ProxmoxAPI('192.168.0.7', user='root@pam', password='NickLQ!709**', verify_ssl=False)
node = proxmox.nodes('pve')
def get_node_cpu():
    node = proxmox.nodes('pve')
    data = node.status.get()
    return(data)

def vm_status():
    for vm in proxmox.cluster.resources.get(type='vm'):
        print("{0}".format(vm['vmid']))

def vm_status2():
    for vm in vm_status():
        print(node.qemu.vm.status.current)



vm_status()

