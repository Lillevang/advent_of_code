private boolean hasDuplicateFagPrisWithSameSyncOperation(SkolefagVM skolefag, SkolefagTillaegsprisVM tillaegspris) {
        int counter = 0;
        for (SkolefagTillaegsprisVM tillaegsprisVM : skolefag.getTillaegsprisVMList()) {
            if (tillaegspris.getTillaegsprisGUID().equals(tillaegsprisVM.getTillaegsprisGUID()) &&
                    tillaegspris.getOperationType().getValue()
                            .equals(tillaegsprisVM.getOperationType().getValue())) {
                if (++counter == 2) {
                    return true;
                }
            }
        }
        for (TillaegsprisVM tillaegsprisVM : hold.getTillaegsprisVMList()) {
            if (tillaegspris.getTillaegsprisGUID().equals(tillaegsprisVM.getTillaegsprisGUID()) &&
                    tillaegspris.getOperationType().getValue().equals(tillaegsprisVM.getOperationType().getValue())) {
                return true;
            }
        }
        return false;
    }
